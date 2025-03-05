import os
from docx import Document
from PyPDF2 import PdfReader
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace with your Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the API key is loaded correctly
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

def summarize_text(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Summarize the following text:\n\n{text}"
    response = model.generate_content(prompt)
    print("Summarize API response:", response)  # Debug print
    return response.text if response.text else "Summarization failed"

def translate_text(text, target_language):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Translate the following text to {target_language}:\n\n{text}\n\nIf the text is already in {target_language}, return it as is."
    response = model.generate_content(prompt)
    print("Translate API response:", response)  # Debug print
    return response.text if response.text else "Translation failed"

def process_file(file, file_type, target_language):
    if file_type == 'pdf':
        text = extract_text_from_pdf(file)
    elif file_type == 'docx':
        text = extract_text_from_docx(file)
    else:
        raise ValueError('Unsupported file format')

    summary = summarize_text(text)
    translated_summary = translate_text(summary, target_language)
    return translated_summary

st.title('Legal Document Summarizer')

uploaded_file = st.file_uploader('Upload a legal document (PDF or DOCX)', type=['pdf', 'docx'])
target_language = st.selectbox('Select the target language', ['en', 'hi', 'mr', 'te'])

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]
    summary = process_file(uploaded_file, file_type, target_language)
    st.write('Summary:', summary)