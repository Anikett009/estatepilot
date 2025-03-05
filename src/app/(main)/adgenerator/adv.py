# # import streamlit as st
# # import requests
# # from dotenv import load_dotenv
# # import os

# # # Load environment variables
# # load_dotenv()

# # REV_API_KEY = os.getenv("REV_API_KEY")
# # REV_APP_ID = os.getenv("REV_APP_ID")

# # # Function to translate text using Reverie Localization API
# # def translate_text(text, source_language, target_language):
# #     url = "https://revapi.reverieinc.com/"
# #     headers = {
# #         "Content-Type": "application/json",
# #         "REV-API-KEY": REV_API_KEY,
# #         "REV-APP-ID": REV_APP_ID,
# #         "src_lang": source_language,
# #         "tgt_lang": target_language,
# #         "domain": "generic",
# #         "REV-APPNAME": "localization",
# #         "REV-APPVERSION": "3.0"
# #     }
# #     data = {
# #         "data": [text],
# #         "nmtMask": True,
# #         "nmtMaskTerms": {
# #             "Reverie Language Technologies": "Reverie Language Technologies"
# #         },
# #         "enableNmt": True,
# #         "enableLookup": True
# #     }
# #     response = requests.post(url, headers=headers, json=data)
# #     if response.status_code == 200:
# #         response_json = response.json()
# #         translated_texts = [item["outString"] for item in response_json["responseList"]]
# #         return translated_texts[0] if translated_texts else "Translation failed."
# #     else:
# #         return "Translation failed."

# # # Streamlit app
# # st.title("Creative Ad Line Generator")

# # # Input ad line
# # ad_line = st.text_input("Enter your creative ad line:")

# # # Generate and translate ad line
# # if st.button("Generate and Translate"):
# #     if ad_line:
# #         st.write(f"Original Ad Line: {ad_line}")
        
# #         # Translate to Hindi
# #         translated_hindi = translate_text(ad_line, "en", "hi")
# #         st.write(f"Translated to Hindi: {translated_hindi}")
        
# #         # Translate to Marathi
# #         translated_marathi = translate_text(ad_line, "en", "mr")
# #         st.write(f"Translated to Marathi: {translated_marathi}")
        
# #         # Translate to Telugu
# #         translated_telugu = translate_text(ad_line, "en", "te")
# #         st.write(f"Translated to Telugu: {translated_telugu}")
# #     else:
# #         st.error("Please enter an ad line.")\
# import streamlit as st
# import requests
# from dotenv import load_dotenv
# import os
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# REV_API_KEY = os.getenv("REV_API_KEY")
# REV_APP_ID = os.getenv("REV_APP_ID")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Configure the Gemini API
# genai.configure(api_key=GEMINI_API_KEY)

# # Function to translate text using Reverie Localization API
# def translate_text(text, source_language, target_language):
#     url = "https://revapi.reverieinc.com/"
#     headers = {
#         "Content-Type": "application/json",
#         "REV-API-KEY": REV_API_KEY,
#         "REV-APP-ID": REV_APP_ID,
#         "src_lang": source_language,
#         "tgt_lang": target_language,
#         "domain": "generic",
#         "REV-APPNAME": "localization",
#         "REV-APPVERSION": "3.0"
#     }
#     data = {
#         "data": [text],
#         "nmtMask": True,
#         "nmtMaskTerms": {
#             "Reverie Language Technologies": "Reverie Language Technologies"
#         },
#         "enableNmt": True,
#         "enableLookup": True
#     }
#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         response_json = response.json()
#         translated_texts = [item["outString"] for item in response_json["responseList"]]
#         return translated_texts[0] if translated_texts else "Translation failed."
#     else:
#         return "Translation failed."

# # Function to generate a creative ad line using Gemini API
# def generate_ad_line(prompt):
#     try:
#         model = genai.GenerativeModel('gemini-2.0-flash')
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         st.error(f"Error generating ad line: {str(e)}")
#         return "Failed to generate ad line."

# # Streamlit app
# st.title("Creative Ad Line Generator")

# # Input prompt
# prompt = st.text_input("Enter your prompt for the ad line:")

# # Generate and translate ad line
# if st.button("Generate and Translate"):
#     if prompt:
#         # Generate ad line in English
#         ad_line = generate_ad_line(prompt)
#         st.write(f"Generated Ad Line in English . Give a proper add line which will help sell my estate fast .Be concise and just give me one catchy tagline (a header) and 2 descriptive lines , nothing more. JUST GIVE ME THE ADDLINE AND 2 DESCRIPTIVE LINES DONT EXPLAIN ANYTHING : {ad_line}")
        
#         # Translate to Hindi
#         translated_hindi = translate_text(ad_line, "en", "hi")
#         st.write(f"Translated to Hindi: {translated_hindi}")
        
#         # Translate to Marathi
#         translated_marathi = translate_text(ad_line, "en", "mr")
#         st.write(f"Translated to Marathi: {translated_marathi}")
        
#         # Translate to Telugu
#         translated_telugu = translate_text(ad_line, "en", "te")
#         st.write(f"Translated to Telugu: {translated_telugu}")
#     else:
#         st.error("Please enter a prompt.")
import streamlit as st
import requests
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import io

# Load environment variables
load_dotenv()

REV_API_KEY = os.getenv("REV_API_KEY")
REV_APP_ID = os.getenv("REV_APP_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to translate text using Reverie Localization API
def translate_text(text, source_language, target_language):
    url = "https://revapi.reverieinc.com/"
    headers = {
        "Content-Type": "application/json",
        "REV-API-KEY": REV_API_KEY,
        "REV-APP-ID": REV_APP_ID,
        "src_lang": source_language,
        "tgt_lang": target_language,
        "domain": "generic",
        "REV-APPNAME": "localization",
        "REV-APPVERSION": "3.0"
    }
    data = {
        "data": [text],
        "nmtMask": True,
        "nmtMaskTerms": {
            "Reverie Language Technologies": "Reverie Language Technologies"
        },
        "enableNmt": True,
        "enableLookup": True
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_json = response.json()
        translated_texts = [item["outString"] for item in response_json["responseList"]]
        return translated_texts[0] if translated_texts else "Translation failed."
    else:
        return "Translation failed."

# Function to generate a creative ad line using Gemini API
def generate_ad_line(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating ad line: {str(e)}")
        return "Failed to generate ad line."

# Function to create a poster
def create_poster(ad_line, language):
    # Load a sample background image
    background = Image.open("background.png")
    draw = ImageDraw.Draw(background)
    
    # Define fonts
    title_font = ImageFont.truetype("arial.ttf", 50)
    description_font = ImageFont.truetype("arial.ttf", 30)
    
    # Split ad line into title and description
    lines = ad_line.split("\n")
    title = lines[0]
    description = "\n".join(lines[1:])
    
    # Add text to image
    draw.text((50, 50), title, font=title_font, fill="black")
    draw.text((50, 150), description, font=description_font, fill="black")
    
    # Save image to a BytesIO object
    img_bytes = io.BytesIO()
    background.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    
    return img_bytes

# Streamlit app
st.title("Creative Ad Line Generator")

# Input prompt
prompt = st.text_input("Enter your prompt for the ad line:")

# Generate and translate ad line
if st.button("Generate and Translate"):
    if prompt:
        prompt = ' Give a proper ad line which will help sell my estate fast .Be concise and just give me one catchy tagline (a header) and 2 descriptive lines , nothing more. JUST GIVE ME THE ADDLINE AND 2 DESCRIPTIVE LINES DONT EXPLAIN ANYTHING .LIMIT ANS TO 50 WORDS.DONT Reccomend me anything I just want a catchy tagline and 2 line describing my prompt.No recommendation . Strict to my add line' + prompt
        # Generate ad line in English
        ad_line = generate_ad_line(prompt)
        st.write(f"Generated Ad Line in English .: {ad_line}")
        
        # Translate to Hindi
        translated_hindi = translate_text(ad_line, "en", "hi")
        st.write(f"Translated to Hindi: {translated_hindi}")
        
        # Translate to Marathi
        translated_marathi = translate_text(ad_line, "en", "mr")
        st.write(f"Translated to Marathi: {translated_marathi}")
        
        # Translate to Telugu
        translated_telugu = translate_text(ad_line, "en", "te")
        st.write(f"Translated to Telugu: {translated_telugu}")
        

    else:
        st.error("Please enter a prompt.")