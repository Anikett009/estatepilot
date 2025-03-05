# import streamlit as st
# import sqlite3
# from typing import Any
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# # Get the API key from the environment variable
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Initialize the Gemini API with the API key
# genai.configure(api_key=GEMINI_API_KEY)

# # Function to generate a response using Gemini API
# def generate_response(context, user_input):
#     try:
#         model = genai.GenerativeModel('gemini-2.0-flash')
#         full_prompt = f"Give ans only in English.You are a professional real estate agent.Explore the current market trends and context which is users conversation/talks in the market ,also answer the users question , use the internet to give lighting fast real estate news of India.Give proper answer of the users question. Context of previous messages:\n{context}\n\nUser input: {user_input}"
#         response = model.generate_content(full_prompt)
#         return response.text
#     except Exception as e:
#         st.error(f"Error generating response: {str(e)}")
#         return "Sorry, I couldn't generate a response."

# # Function to fetch properties from the database
# def fetch_properties(city: str) -> list[dict[str, Any]]:
#     conn = sqlite3.connect("house.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT city, price, location, builder, possession_status, likes, dislikes FROM properties WHERE city = ? ORDER BY likes DESC, dislikes ASC LIMIT 2", (city,))
#     rows = cursor.fetchall()
#     conn.close()
    
#     properties = []
#     for row in rows:
#         properties.append({
#             "city": row[0],
#             "price": row[1],
#             "location": row[2],
#             "builder": row[3],
#             "possession_status": row[4],
#             "likes": row[5],
#             "dislikes": row[6]
#         })
    
#     return properties

# # Function to update likes and dislikes
# def update_feedback(city: str, price: str, feedback: str):
#     conn = sqlite3.connect("house.db")
#     cursor = conn.cursor()
#     if feedback == "like":
#         cursor.execute("UPDATE properties SET likes = likes + 1 WHERE city = ? AND price = ?", (city, price))
#     elif feedback == "dislike":
#         cursor.execute("UPDATE properties SET likes = likes - 1 WHERE city = ? AND price = ?", (city, price))
#     conn.commit()
#     conn.close()

# # Streamlit app
# st.title("Real Estate Chatbot")

# context = st.session_state.get("context", "")
# user_input = st.text_input("Enter your query about the flat and city:")

# if st.button("Ask"):
#     if user_input:
#         response = generate_response(context, user_input)
#         st.session_state.context = context + f"\nUser: {user_input}\nBot: {response}\n"
#         st.write(response)
        
#         city = user_input.split()[-1]
#         properties = fetch_properties(city)
        
#         if properties:
#             st.write("Here are some properties you might be interested in:")
#             for prop in properties:
#                 st.write(f"City: {prop['city']}")
#                 st.write(f"Price: {prop['price']}")
#                 st.write(f"Location: {prop['location']}")
#                 st.write(f"Builder: {prop['builder']}")
#                 st.write(f"Possession Status: {prop['possession_status']}")
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     if st.button("Like", key=f"like_{prop['city']}_{prop['price']}"):
#                         update_feedback(prop['city'], prop['price'], "like")
#                         st.write("You liked this property.")
#                         st.success("Feedback saved successfully.")
#                 with col2:
#                     if st.button("Dislike", key=f"dislike_{prop['city']}_{prop['price']}"):
#                         update_feedback(prop['city'], prop['price'], "dislike")
#                         st.write("You disliked this property.")
#                         st.success("Feedback saved successfully.")
#         else:
#             st.write("No properties found for the specified city.")
#     else:
#         st.error("Please enter a query.")
import streamlit as st
import sqlite3
from typing import Any
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini API with the API key
genai.configure(api_key=GEMINI_API_KEY)

# Function to generate a response using Gemini API
def generate_response(context, user_input):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        full_prompt = f"Give ans only in English.Don't mention current date.You are a professional real estate agent.Explore the current market trends and context which is users conversation/talks in the market ,also answer the users question , use the internet to give lighting fast real estate news of India.Give proper answer of the users question. Context of previous messages:\n{context}\n\nUser input: {user_input}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "Sorry, I couldn't generate a response."

# Function to fetch properties from the database
def fetch_properties(city: str) -> list[dict[str, Any]]:
    conn = sqlite3.connect("house.db")
    cursor = conn.cursor()
    cursor.execute("SELECT city, price, location, builder, possession_status, likes, dislikes FROM properties WHERE city = ? ORDER BY likes DESC, dislikes ASC LIMIT 2", (city,))
    rows = cursor.fetchall()
    conn.close()
    
    properties = []
    for row in rows:
        properties.append({
            "city": row[0],
            "price": row[1],
            "location": row[2],
            "builder": row[3],
            "possession_status": row[4],
            "likes": row[5],
            "dislikes": row[6]
        })
    
    return properties

# Function to update likes and dislikes
def update_feedback(city: str, price: str, feedback: str):
    conn = sqlite3.connect("house.db")
    cursor = conn.cursor()
    if feedback == "like":
        cursor.execute("UPDATE properties SET likes = likes + 1 WHERE city = ? AND price = ?", (city, price))
    elif feedback == "dislike":
        cursor.execute("UPDATE properties SET likes = likes - 1 WHERE city = ? AND price = ?", (city, price))
    conn.commit()
    conn.close()

# Streamlit app
st.title("Real Estate Chatbot")

context = st.session_state.get("context", "")
user_input = st.text_input("Enter your query about the flat and city:")

if st.button("Ask"):
    if user_input:
        response = generate_response(context, user_input)
        st.session_state.context = context + f"\nUser: {user_input}\nBot: {response}\n"
        st.write(response)
        
        city = user_input.split()[-1]
        properties = fetch_properties(city)
        st.session_state.properties = properties
        
if "properties" in st.session_state:
    properties = st.session_state.properties
    if properties:
        st.write("Here are some properties you might be interested in:")
        for prop in properties:
            st.write(f"City: {prop['city']}")
            st.write(f"Price: {prop['price']}")
            st.write(f"Location: {prop['location']}")
            st.write(f"Builder: {prop['builder']}")
            st.write(f"Possession Status: {prop['possession_status']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Like", key=f"like_{prop['city']}_{prop['price']}"):
                    update_feedback(prop['city'], prop['price'], "like")
                    st.write("You liked this property.")
                    st.success("Feedback saved successfully.")
            with col2:
                if st.button("Dislike", key=f"dislike_{prop['city']}_{prop['price']}"):
                    update_feedback(prop['city'], prop['price'], "dislike")
                    st.write("You disliked this property.")
                    st.success("Feedback saved successfully.")
    else:
        st.write("No properties found for the specified city.")
else:
    st.write("Please enter a query and press 'Ask'.")