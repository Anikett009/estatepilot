import streamlit as st
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
import os
from streamlit_chat import message
# Load environment variables
load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

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
    return messages[::-1]  # Reverse to get the correct order

# Function to generate a response using Gemini API
def generate_response(context, user_input):
    try:
        # Create the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Combine context and user input
        full_prompt = f"Give ans only in English.You are a professional real estate agent.Explore the current market trends and context which is users conversation/talks in the market ,also answer the users question , use the internet to give lighting fast real estate news of India.Give proper answer of the users question. Context of previous messages:\n{context}\n\nUser input: {user_input}"
        
        # Generate response    
        response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "Sorry, I couldn't generate a response."

# Streamlit app
def main():
    st.title("Real Estate Agent Chatbot")


    messages = get_last_10_messages()
    context = ""
    for msg in messages:
        context += f"{msg[0]}: {msg[1]} ({msg[2]})\n"
        

    # User input
    user_input = st.text_input("You:")

    # Generate response
    if st.button("Send"):
        if user_input:
            response = generate_response(context, user_input)
            st.write(f"Bot: {response}")
        else:
            st.error("Please enter a message.")

if __name__ == "__main__":
    main()