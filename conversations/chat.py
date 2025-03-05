# # import streamlit as st
# # import sqlite3
# # import time
# # from streamlit_server_state import server_state, server_state_lock

# # # SQLite setup
# # def init_db():
# #     conn = sqlite3.connect("chat.db", check_same_thread=False)
# #     cursor = conn.cursor()
# #     cursor.execute("""
# #     CREATE TABLE IF NOT EXISTS messages (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         sender TEXT,
# #         receiver TEXT,
# #         message TEXT,
# #         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
# #     )
# #     """)
# #     conn.commit()
# #     return conn

# # conn = init_db()

# # # Function to insert messages
# # def insert_message(sender, receiver, message):
# #     cursor = conn.cursor()
# #     cursor.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)",
# #                    (sender, receiver, message))
# #     conn.commit()

# # # Function to fetch messages
# # def get_messages(user1, user2):
# #     cursor = conn.cursor()
# #     cursor.execute("""
# #     SELECT sender, message, timestamp FROM messages
# #     WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)
# #     ORDER BY timestamp
# #     """, (user1, user2, user2, user1))
# #     return cursor.fetchall()

# # # Streamlit login/logout logic
# # st.session_state.setdefault("logged_in", False)
# # st.session_state.setdefault("username", "")
# # st.session_state.setdefault("receiver", "")

# # if not st.session_state.logged_in:
# #     st.title("Login")
# #     username = st.text_input("Enter your username:")
# #     if st.button("Login"):
# #         if username.strip():
# #             st.session_state.logged_in = True
# #             st.session_state.username = username.strip()
            
# # else:
# #     st.title(f"Chat - {st.session_state.username}")
# #     receiver = st.text_input("Chat with:", key="receiver_input")
# #     if receiver:
# #         st.session_state.receiver = receiver
    
# #     # Chat UI
# #     chat_container = st.container()
# #     message_input = st.text_input("Type a message:", key="message_input")
    
# #     if st.button("Send") and message_input:
# #         insert_message(st.session_state.username, st.session_state.receiver, message_input)
# #         with server_state_lock["messages"]:
# #             if "messages" not in server_state:
# #                 server_state["messages"] = []
# #             server_state["messages"].append({
# #                 "sender": st.session_state.username,
# #                 "receiver": st.session_state.receiver,
# #                 "message": message_input,
# #                 "timestamp": time.time()
# #             })
        
    
# #     # Fetch and display messages
# #     messages = get_messages(st.session_state.username, st.session_state.receiver)
# #     with chat_container:
# #         for msg in messages:
# #             st.write(f"{msg[0]}: {msg[1]} ({msg[2]})")
    
# #     if st.button("Logout"):
# #         st.session_state.logged_in = False
# #         st.session_state.username = ""
        

# # # Function to update messages in real-time
# # def update_messages():
# #     while True:
# #         time.sleep(1)
        

# # # Start a thread to update messages in real-time
# # import threading
# # threading.Thread(target=update_messages, daemon=True).start()
# import streamlit as st
# import sqlite3
# import time
# from streamlit_server_state import server_state, server_state_lock

# # SQLite setup
# def init_db():
#     conn = sqlite3.connect("chat.db", check_same_thread=False)
#     cursor = conn.cursor()
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS messages (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         sender TEXT,
#         receiver TEXT,
#         message TEXT,
#         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
#     """)
#     conn.commit()
#     return conn

# conn = init_db()

# # Function to insert messages
# def insert_message(sender, receiver, message):
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)",
#                    (sender, receiver, message))
#     conn.commit()

# # Function to fetch messages
# def get_messages(user1, user2):
#     cursor = conn.cursor()
#     cursor.execute("""
#     SELECT sender, message, timestamp FROM messages
#     WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)
#     ORDER BY timestamp
#     """, (user1, user2, user2, user1))
#     return cursor.fetchall()

# # Streamlit login/logout logic
# st.session_state.setdefault("logged_in", False)
# st.session_state.setdefault("username", "")
# st.session_state.setdefault("receiver", "")

# if not st.session_state.logged_in:
#     st.title("Login")
#     username = st.text_input("Enter your username:")
#     if st.button("Login"):
#         if username.strip():
#             st.session_state.logged_in = True
#             st.session_state.username = username.strip()
            
# else:
#     st.sidebar.title(f"Logged in as {st.session_state.username}")
#     receiver = st.sidebar.selectbox("Chat with:", ["Yash", "Aniket", "Aviraj"])
#     if receiver and receiver != st.session_state.username:
#         st.session_state.receiver = receiver
    
#     # Chat UI
#     st.title(f"Chat with {st.session_state.receiver}")
#     chat_container = st.container()
#     message_input = st.text_input("Type a message:", key="message_input")
    
#     if st.button("Send") and message_input:
#         insert_message(st.session_state.username, st.session_state.receiver, message_input)
#         with server_state_lock["messages"]:
#             if "messages" not in server_state:
#                 server_state["messages"] = []
#             server_state["messages"].append({
#                 "sender": st.session_state.username,
#                 "receiver": st.session_state.receiver,
#                 "message": message_input,
#                 "timestamp": time.time()
#             })

    
#     # Fetch and display messages
#     messages = get_messages(st.session_state.username, st.session_state.receiver)
#     with chat_container:
#         for msg in messages:
#             if msg[0] == st.session_state.username:
#                 st.markdown(f"""
#                 <div style='text-align: right; margin: 10px;'>
#                     <div style='display: inline-block; background-color: #DCF8C6; padding: 10px; border-radius: 10px;'>
#                         <b>{msg[0]}</b>: {msg[1]} <i>({msg[2]})</i>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div style='text-align: left; margin: 10px;'>
#                     <div style='display: inline-block; background-color: #FFFFFF; padding: 10px; border-radius: 10px;'>
#                         <b>{msg[0]}</b>: {msg[1]} <i>({msg[2]})</i>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
    
#     if st.sidebar.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = ""


# # Function to update messages in real-time
# def update_messages():
#     while True:
#         time.sleep(1)
       

# # Start a thread to update messages in real-time
# import threading
# threading.Thread(target=update_messages, daemon=True).start()
# import streamlit as st
# import sqlite3
# import time

# # SQLite setup
# def init_db():
#     conn = sqlite3.connect("chat.db", check_same_thread=False)
#     cursor = conn.cursor()
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS messages (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         sender TEXT,
#         receiver TEXT,
#         message TEXT,
#         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
#     """)
#     conn.commit()
#     return conn

# conn = init_db()

# # Function to insert messages
# def insert_message(sender, receiver, message):
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)",
#                    (sender, receiver, message))
#     conn.commit()

# # Function to fetch messages
# def get_messages(user1, user2):
#     cursor = conn.cursor()
#     cursor.execute("""
#     SELECT sender, message, timestamp FROM messages
#     WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)
#     ORDER BY timestamp
#     """, (user1, user2, user2, user1))
#     return cursor.fetchall()

# # Streamlit login/logout logic
# st.session_state.setdefault("logged_in", False)
# st.session_state.setdefault("username", "")
# st.session_state.setdefault("receiver", "")
# st.session_state.setdefault("last_check", time.time())

# if not st.session_state.logged_in:
#     st.title("Login")
#     username = st.text_input("Enter your username:")
#     if st.button("Login"):
#         if username.strip():
#             st.session_state.logged_in = True
#             st.session_state.username = username.strip()
           
# else:
#     st.sidebar.title(f"Logged in as {st.session_state.username}")
#     receiver = st.sidebar.selectbox("Chat with:", ["Yash", "Aniket", "Aviraj"])
#     if receiver and receiver != st.session_state.username:
#         st.session_state.receiver = receiver
    
#     # Chat UI
#     st.title(f"Chat with {st.session_state.receiver}")
#     chat_container = st.container()
#     message_input = st.text_input("Type a message:", key="message_input")
    
#     if st.button("Send") and message_input:
#         insert_message(st.session_state.username, st.session_state.receiver, message_input)
     
    
#     # Fetch and display messages
#     messages = get_messages(st.session_state.username, st.session_state.receiver)
#     with chat_container:
#         for msg in messages:
#             if msg[0] == st.session_state.username:
#                 st.markdown(f"""
#                 <div style='text-align: right; margin: 10px;'>
#                     <div style='display: inline-block; background-color: #DCF8C6; padding: 10px; border-radius: 10px;'>
#                         <b>{msg[0]}</b>: {msg[1]} <i>({msg[2]})</i>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div style='text-align: left; margin: 10px;'>
#                     <div style='display: inline-block; background-color: #FFFFFF; padding: 10px; border-radius: 10px;'>
#                         <b>{msg[0]}</b>: {msg[1]} <i>({msg[2]})</i>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
    
#     if st.sidebar.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = ""

# # Function to update messages in real-time
# def update_messages():
#     while True:
#         time.sleep(5)
        

# # Start a thread to update messages in real-time
# import threading
# threading.Thread(target=update_messages, daemon=True).start()
# import streamlit as st
# import sqlite3
# import time
# import requests
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# REV_API_KEY = os.getenv("REV_API_KEY")
# REV_APP_ID = os.getenv("REV_APP_ID")

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

# # SQLite setup
# def init_db():
#     conn = sqlite3.connect("chat.db", check_same_thread=False)
#     cursor = conn.cursor()
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS messages (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         sender TEXT,
#         receiver TEXT,
#         message TEXT,
#         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
#     """)
#     conn.commit()
#     return conn

# conn = init_db()

# # Function to insert messages
# def insert_message(sender, receiver, message):
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)",
#                    (sender, receiver, message))
#     conn.commit()

# # Function to fetch messages
# def get_messages(user1, user2):
#     cursor = conn.cursor()
#     cursor.execute("""
#     SELECT sender, message, timestamp FROM messages
#     WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)
#     ORDER BY timestamp
#     """, (user1, user2, user2, user1))
#     return cursor.fetchall()

# # Streamlit login/logout logic
# st.session_state.setdefault("logged_in", False)
# st.session_state.setdefault("username", "")
# st.session_state.setdefault("receiver", "")
# st.session_state.setdefault("mother_tongue", "")

# # Define mother tongues for users
# user_mother_tongues = {
#     "Yash": "en",
#     "Aniket": "mr",
#     "Aviraj": "hi"
# }

# if not st.session_state.logged_in:
#     st.title("Login")
#     username = st.text_input("Enter your username:")
#     if st.button("Login"):
#         if username.strip() in user_mother_tongues:
#             st.session_state.logged_in = True
#             st.session_state.username = username.strip()
#             st.session_state.mother_tongue = user_mother_tongues[username.strip()]
#         else:
#             st.error("Invalid username! Only Yash, Aniket, and Aviraj are allowed.")
# else:
#     st.sidebar.title(f"Logged in as {st.session_state.username}")
#     receiver = st.sidebar.selectbox("Chat with:", ["Yash", "Aniket", "Aviraj"])
#     if receiver and receiver != st.session_state.username:
#         st.session_state.receiver = receiver
    
#     # Chat UI
#     st.title(f"Chat with {st.session_state.receiver}")
#     chat_container = st.container()
#     message_input = st.text_input("Type a message:", key="message_input")
    
#     if st.button("Send") and message_input:
#         # Translate the message to the receiver's mother tongue
#         translated_message = translate_text(message_input, st.session_state.mother_tongue, user_mother_tongues[st.session_state.receiver])
#         insert_message(st.session_state.username, st.session_state.receiver, translated_message)
#         st.experimental_rerun()
    
#     # Fetch and display messages
#     messages = get_messages(st.session_state.username, st.session_state.receiver)
#     with chat_container:
#         for msg in messages[-10:]:  # Display the last 10 messages
#             if msg[0] == st.session_state.username:
#                 st.markdown(f"""
#                 <div style='text-align: right; margin: 10px;'>
#                     <div style='display: inline-block; background-color: #DCF8C6; padding: 10px; border-radius: 10px;'>
#                         <b>{msg[0]}</b>: {msg[1]} <i>({msg[2]})</i>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div style='text-align: left; margin: 10px;'>
#                     <div style='display: inline-block; background-color: #FFFFFF; padding: 10px; border-radius: 10px;'>
#                         <b>{msg[0]}</b>: {msg[1]} <i>({msg[2]})</i>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
    
#     if st.sidebar.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = ""

# # Function to update messages in real-time
# def update_messages():
#     while True:
#         time.sleep(5)
#         st.experimental_rerun()

# # Start a thread to update messages in real-time
# import threading
# threading.Thread(target=update_messages, daemon=True).start()
import streamlit as st
import sqlite3
import time
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

REV_API_KEY = os.getenv("REV_API_KEY")
REV_APP_ID = os.getenv("REV_APP_ID")

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

# SQLite setup
def init_db(db_name):
    conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    return conn

# Initialize databases
main_conn = init_db("chat.db")
yash_conn = init_db("yash_chat.db")
aniket_conn = init_db("aniket_chat.db")
aviraj_conn = init_db("aviraj_chat.db")

# Function to insert messages
def insert_message(conn, sender, receiver, message):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)",
                   (sender, receiver, message))
    conn.commit()

# Function to fetch messages
def get_messages(conn, user1, user2):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT sender, message, timestamp FROM messages
    WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)
    ORDER BY timestamp
    """, (user1, user2, user2, user1))
    return cursor.fetchall()

# Streamlit login/logout logic
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("receiver", "")
st.session_state.setdefault("mother_tongue", "")

# Define mother tongues for users
user_mother_tongues = {
    "Yash": "en",
    "Aniket": "mr",
    "Aviraj": "hi"
}

if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Enter your username:")
    if st.button("Login"):
        if username.strip() in user_mother_tongues:
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.session_state.mother_tongue = user_mother_tongues[username.strip()]
        else:
            st.error("Invalid username! Only Yash, Aniket, and Aviraj are allowed.")
else:
    st.sidebar.title(f"Logged in as {st.session_state.username}")
    receiver = st.sidebar.selectbox("Chat with:", ["Yash", "Aniket", "Aviraj"])
    if receiver and receiver != st.session_state.username:
        st.session_state.receiver = receiver
    
    # Chat UI
    st.title(f"Chat with {st.session_state.receiver}")
    chat_container = st.container()
    message_input = st.text_input("Type a message:", key="message_input")
    
    if st.button("Send") and message_input:
        # Translate the message to English before storing it in the main database
        translated_message_to_english = translate_text(message_input, st.session_state.mother_tongue, "en")
        insert_message(main_conn, st.session_state.username, st.session_state.receiver, translated_message_to_english)
        
        # Translate the message to the receiver's mother tongue and store it in their database
        translated_message_to_receiver = translate_text(message_input, st.session_state.mother_tongue, user_mother_tongues[st.session_state.receiver])
        if st.session_state.receiver == "Yash":
            insert_message(yash_conn, st.session_state.username, st.session_state.receiver, translated_message_to_receiver)
        elif st.session_state.receiver == "Aniket":
            insert_message(aniket_conn, st.session_state.username, st.session_state.receiver, translated_message_to_receiver)
        elif st.session_state.receiver == "Aviraj":
            insert_message(aviraj_conn, st.session_state.username, st.session_state.receiver, translated_message_to_receiver)

    
    # Fetch and display messages
    if st.session_state.username == "Yash":
        messages = get_messages(yash_conn, st.session_state.username, st.session_state.receiver)
    elif st.session_state.username == "Aniket":
        messages = get_messages(aniket_conn, st.session_state.username, st.session_state.receiver)
    elif st.session_state.username == "Aviraj":
        messages = get_messages(aviraj_conn, st.session_state.username, st.session_state.receiver)
    
    with chat_container:
        for msg in messages[-10:]:  # Display the last 10 messages
            if msg[0] == st.session_state.username:
                st.markdown(f"""
                <div style='text-align: right; margin: 10px;'>
                    <div style='display: inline-block; background-color: #DCF8C6; padding: 10px; border-radius: 10px;'>
                        <b>{msg[0]}</b>: {msg[1]} <i>({msg[2]})</i>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='text-align: left; margin: 10px;'>
                    <div style='display: inline-block; background-color: #FFFFFF; padding: 10px; border-radius: 10px;'>
                        <b>{msg[0]}</b>: {msg[1]} <i>({msg[2]})</i>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""

# Function to update messages in real-time
def update_messages():
    while True:
        time.sleep(5)
      

# Start a thread to update messages in real-time
import threading
threading.Thread(target=update_messages, daemon=True).start()