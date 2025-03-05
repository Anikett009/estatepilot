from flask import Flask, request, jsonify
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

# Function to fetch the last 10 messages from chat.db
def get_last_10_messages():
    conn = sqlite3.connect("chat.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT sender, message, timestamp FROM messages
    ORDER BY timestamp DESC LIMIT 10
    """)
    messages = cursor.fetchall()
    conn.close()

    # Format messages as context
    context = "\n".join([f"{msg[0]}: {msg[1]} ({msg[2]})" for msg in messages[::-1]])
    return context

# Function to generate a response using Gemini API
def generate_response(context, user_input):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Prompt format
        full_prompt = (
            f"Give answer only in English. You are a professional real estate agent. "
            f"Explore the current market trends and context from users' conversations, "
            f"answer the user's question, and use the internet for real-time real estate news in India. "
            f"Provide proper answers. Context of previous messages:\n{context}\n\nUser input: {user_input}"
        )

        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Flask route to handle user queries
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get JSON input
        data = request.json
        user_input = data.get("message", "")

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        # Fetch previous chat context
        context = get_last_10_messages()

        # Generate response
        response = generate_response(context, user_input)

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask server
if __name__ == "__main__":
    import hypercorn.asyncio
    from hypercorn.config import Config

    config = Config()
    config.bind = ["localhost:5001"]  # Set host & port

    import asyncio
    asyncio.run(hypercorn.asyncio.serve(app, config))
