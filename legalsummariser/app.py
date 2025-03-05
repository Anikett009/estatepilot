import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from docx import Document
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''.join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

def summarize_text(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Summarize the following text:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text if response.text else "Summarization failed"

def translate_text(text, target_language):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Translate the following text to {target_language}:\n\n{text}\n\nIf the text is already in {target_language}, return it as is.Do not mention that you are an AI agent and that you have limited capabilities"
    response = model.generate_content(prompt)
    return response.text if response.text else "Translation failed"

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files or 'target_language' not in request.form:
        return jsonify({"error": "Missing file or language"}), 400

    file = request.files['file']
    target_language = request.form['target_language']
    file_type = file.filename.split('.')[-1].lower()

    if file_type not in ['pdf', 'docx']:
        return jsonify({"error": "Unsupported file format"}), 400

    # Extract text
    text = extract_text_from_pdf(file) if file_type == 'pdf' else extract_text_from_docx(file)

    # Summarize & Translate
    summary = summarize_text(text)
    translated_summary = translate_text(summary, target_language)

    return jsonify({"summary": translated_summary})

# Run with Hypercorn
if __name__ == "__main__":
    import hypercorn.asyncio
    from hypercorn.config import Config
    import asyncio

    config = Config()
    config.bind = ["localhost:5003"]  # Set host & port

    asyncio.run(hypercorn.asyncio.serve(app, config))
