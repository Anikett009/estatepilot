import os
import httpx
import asyncio
import google.generativeai as genai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from hypercorn.asyncio import serve
from hypercorn.config import Config
from flask_cors import CORS

# Load environment variables
load_dotenv()

REV_API_KEY = os.getenv("REV_API_KEY")
REV_APP_ID = os.getenv("REV_APP_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

# Async function to translate text
async def translate_text(text: str, target_language: str):
    url = "https://revapi.reverieinc.com/"
    headers = {
        "Content-Type": "application/json",
        "REV-API-KEY": REV_API_KEY,
        "REV-APP-ID": REV_APP_ID,
        "src_lang": "en",
        "tgt_lang": target_language,
        "domain": "generic",
        "REV-APPNAME": "localization",
        "REV-APPVERSION": "3.0"
    }
    data = {
        "data": [text],
        "nmtMask": True,
        "nmtMaskTerms": {"Reverie Language Technologies": "Reverie Language Technologies"},
        "enableNmt": True,
        "enableLookup": True
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_json = response.json()
            translated_texts = [item["outString"] for item in response_json["responseList"]]
            return translated_texts[0] if translated_texts else "Translation failed."
        return "Translation failed."

# Async function to generate an ad line using Gemini API
async def generate_ad_line(prompt: str):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating ad line: {str(e)}"

@app.route('/generate_and_translate', methods=['POST'])
def generate_and_translate():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    async def process():
        ad_line = await generate_ad_line(prompt)

        # Run translations concurrently
        translations = await asyncio.gather(
            translate_text(ad_line, "hi"),
            translate_text(ad_line, "mr"),
            translate_text(ad_line, "te")
        )

        return {
            "ad_line_english": ad_line,
            "ad_line_hindi": translations[0],
            "ad_line_marathi": translations[1],
            "ad_line_telugu": translations[2]
        }

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(process())

    return jsonify(result)

if __name__ == "__main__":
    config = Config()
    config.bind = ["localhost:5000"]
    asyncio.run(serve(app, config))
