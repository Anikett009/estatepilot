import streamlit as st
from audio_recorder_streamlit import audio_recorder
import assemblyai as aai
import io
from dotenv import load_dotenv
import os
import time
import re
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import speech_recognition as sr
from googletrans import Translator
import wave

# Load environment variables from .env file
load_dotenv()

# Set API Keys
aai.settings.api_key = os.getenv("ASSEMBLY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

def transcribe_audio(audio_data, language_code="en"):
    try:
        config = aai.TranscriptionConfig(language_code=language_code)
        audio_io = io.BytesIO(audio_data)
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_io, config=config)
        
        if transcript.status == aai.TranscriptStatus.error:
            return f"Transcription failed: {transcript.error}"
        return transcript.text
    except Exception as e:
        return f"Error in transcription: {str(e)}"

def translate_to_english(text):
    """
    Translate Hindi text to English using Gemini as a workaround.
    In production, use Google Translate API for better accuracy.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Translate the following Hindi text to English:\n\n{text}\n\nIf the text is already in English, return it as is."
    response = model.generate_content(prompt)
    return response.text if response.text else text

def refine_speech(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"You are a real estate agent. Suggest suitable listings based on my query:\n\nQuery: {text}\n\n."
    
    response = model.generate_content(prompt)
    return response.text if response.text else "Speech refinement failed"

def extract_event_details(text):
    """
    Robust event details extraction with improved date and time parsing.
    Supports various input formats like:
    - "Keep a meeting on 13 March, 5pm with Aniket"
    - "Keep a meeting on 31st December with Yash"
    - "Keep a meeting next tuesday at 5pm"
    - "Schedule a call tomorrow at 2:30 pm"
    """
    event_details = {
        "title": "Meeting",  # Default title, adjusted based on context
        "location": "TBD",  # Default location if not mentioned
        "start_time": None,
        "end_time": None,
        "attendees": [],
        "description": text
    }

    # Extract attendee
    attendee_match = re.search(r'with\s+([A-Za-z\s]+?)(?:\s+on|\s+at|$)', text, re.IGNORECASE)
    if attendee_match:
        attendee_name = attendee_match.group(1).strip()
        event_details["attendees"].append({"name": attendee_name})
        event_details["title"] = f"Meeting with {attendee_name}"

    # Comprehensive date and time extraction
    current_date = datetime.now()

    # Define patterns for different date formats
    date_patterns = [
        r'\b(?:on\s+)?(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+(?:\s+\d{2,4})?)',  # "13 March" or "31st December 2024"
        r'\b(next\s+[A-Za-z]+day)\b',  # "next tuesday"
        r'\b(tomorrow)\b',  # "tomorrow"
        r'\b(today)\b'  # "today"
    ]

    # Define time patterns
    time_patterns = [
        r'\b(?:at|by|around)\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\b',  # "at 5pm", "at 2:30 pm"
    ]

    # Try to extract date
    event_date = current_date
    date_match = None
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_match = match.group(1)
            break

    # Parse extracted date
    if date_match:
        try:
            if "next" in date_match.lower():
                # Handle "next <weekday>"
                day_str = date_match.split()[1].capitalize()
                target_weekday = datetime.strptime(day_str, '%A').weekday()
                current_weekday = current_date.weekday()
                days_ahead = (target_weekday - current_weekday + 7) % 7
                event_date = current_date + timedelta(days=days_ahead)
            elif date_match.lower() == 'tomorrow':
                event_date = current_date + timedelta(days=1)
            elif date_match.lower() == 'today':
                event_date = current_date
            else:
                # Parse dates like "13 March" or "31st December"
                event_date = parse_date(date_match, fuzzy=True, default=current_date)
                
                # Handle year ambiguity
                if event_date.year == current_date.year:
                    if event_date < current_date:
                        event_date = event_date.replace(year=current_date.year + 1)
        except Exception as e:
            st.warning(f"Date parsing error: {e}")

    # Try to extract time
    time_match = None
    for pattern in time_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            time_match = match.group(1)
            break

    # Parse extracted time
    try:
        if time_match:
            # Custom time parsing to handle various formats
            time_match = time_match.lower().replace(' ', '')
            
            # Add AM/PM if missing
            if not re.search(r'am|pm', time_match):
                time_match += 'pm'  # Default to PM if not specified
            
            # Handle formats with and without minutes
            if ':' not in time_match:
                time_match = time_match.replace('am', ':00am').replace('pm', ':00pm')
            
            # Parse time
            start_time = datetime.strptime(f"{event_date.strftime('%Y-%m-%d')} {time_match}", '%Y-%m-%d %I:%M%p')
        else:
            # Default to next full hour
            start_time = current_date.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

        # Ensure event time is in the future
        if start_time <= current_date:
            start_time += timedelta(days=1)

        event_details["start_time"] = start_time
    except Exception as e:
        st.warning(f"Time parsing error: {e}")
        # Fallback time
        event_details["start_time"] = current_date.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    # Duration handling
    duration_match = re.search(r'for\s+(\d+)\s*(hour|minute|hr|min)s?', text, re.IGNORECASE)
    if duration_match and event_details["start_time"]:
        duration_value = int(duration_match.group(1))
        duration_unit = duration_match.group(2).lower()
        
        if "hour" in duration_unit or "hr" in duration_unit:
            event_details["end_time"] = event_details["start_time"] + timedelta(hours=duration_value)
        elif "minute" in duration_unit or "min" in duration_unit:
            event_details["end_time"] = event_details["start_time"] + timedelta(minutes=duration_value)
    else:
        # Default 1-hour duration
        event_details["end_time"] = event_details["start_time"] + timedelta(hours=1)

    return event_details

def get_google_calendar_service():
    """
    Authenticate and return Google Calendar service.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        st.error(f"An error occurred with Google Calendar API: {error}")
        return None

def create_calendar_event(event_details):
    """
    Create an event in Google Calendar based on extracted details.
    """
    service = get_google_calendar_service()
    if not service:
        return False, None

    event = {
        'summary': event_details["title"],
        'location': event_details["location"],
        'description': event_details["description"],
        'start': {
            'dateTime': event_details["start_time"].isoformat(),
            'timeZone': 'Asia/Kolkata',  # Adjust based on your timezone
        },
        'end': {
            'dateTime': event_details["end_time"].isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [{'email': attendee['name'].replace(' ', '.') + '@example.com'} for attendee in event_details["attendees"]],  # Dummy emails
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        event_link = event.get('htmlLink')
        return True, event_link
    except HttpError as error:
        st.error(f"Failed to create event: {error}")
        return False, None

def recognize_and_translate(audio_file, source_language):
    recognizer = sr.Recognizer()
    translator = Translator()
    
    # Convert audio file to wav format
    with wave.open(audio_file, 'rb') as audio:
        with wave.open("temp.wav", 'wb') as temp_audio:
            temp_audio.setnchannels(audio.getnchannels())
            temp_audio.setsampwidth(audio.getsampwidth())
            temp_audio.setframerate(audio.getframerate())
            temp_audio.writeframes(audio.readframes(audio.getnframes()))
    
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        try:
            # Recognize speech
            text = recognizer.recognize_google(audio_data, language=source_language)
            st.write(f"Recognized Text: {text}")
            
            # Use Gemini for translation instead of googletrans
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"Translate the following text to English:\n\n{text}"
            response = model.generate_content(prompt)
            translated_text = response.text if response.text else text
            
            return translated_text
        except sr.UnknownValueError:
            return "Speech recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

def main():
    st.title("Real Estate Analyzer")

    # Language selection
    st.subheader("Select Language")
    language = st.selectbox("Choose the language of your speech input:", ["English", "Hindi", "Marathi", "Telugu"], index=0)
    language_code = {
        "English": "en",
        "Hindi": "hi",
        "Marathi": "mr",
        "Telugu": "te"
    }[language]

    # Record audio
    audio_bytes = audio_recorder(
        energy_threshold=(-1.0, 1.0),
        pause_threshold=60.0,
        sample_rate=41000,
        text="",
        recording_color="#e8b62c",
        neutral_color="#6aa36f",
        icon_name="microphone",
        icon_size="6x"
    )
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.success("Recording completed!")
        
        start_time = time.time()
        
        # Transcribe audio
        if language in ["Marathi", "Telugu"]:
            transcript_text = recognize_and_translate(io.BytesIO(audio_bytes), language_code)
        else:
            transcript_text = transcribe_audio(audio_bytes, language_code=language_code)
        
        st.subheader("Transcription:")
        st.write(transcript_text)
        
        if "failed" in transcript_text.lower():
            st.error("Transcription failed. Please try again.")
            return
        
        # Translate to English if Hindi is selected
        processed_text = transcript_text
        if language == "Hindi":
            processed_text = translate_to_english(transcript_text)
            st.subheader("Translated to English:")
            st.write(processed_text)

        # Extract event details and schedule on Google Calendar
        st.subheader("Event Scheduling:")
        event_details = extract_event_details(processed_text)
        st.write("Extracted Event Details:", event_details)

        if event_details["start_time"] and event_details["end_time"]:
            success, event_url = create_calendar_event(event_details)
            if success:
                st.success("Event successfully scheduled in Google Calendar!")
                st.markdown(f'<a href="{event_url}" target="_blank"><button>Click here to view the event</button></a>', unsafe_allow_html=True)
            else:
                st.error("Failed to schedule event in Google Calendar.")
        else:
            st.warning("Could not extract sufficient details to schedule an event.")

        # Refine Speech
        refined_speech = refine_speech(processed_text)
        st.subheader("Refined Speech:")
        st.write(refined_speech)
        
        duration = time.time() - start_time
        st.write(f"Completed in {duration:.2f} seconds")

if __name__ == "__main__":
    main()