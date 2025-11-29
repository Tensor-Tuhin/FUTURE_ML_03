import streamlit as st
from app import bot_reply

st.title("Spotify Support Chatbot")

if "bot_state" not in st.session_state:
    st.session_state.bot_state = {}
if "messages" not in st.session_state:
    st.session_state.messages = []

for role,text in st.session_state.messages:
    st.chat_message(role).markdown(text)

user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.messages.append(("user",user_input))
    st.chat_message("user").markdown(user_input)

    reply = bot_reply(user_input,st.session_state)
    st.session_state.messages.append(("assistant",reply))
    st.chat_message("assistant").markdown(reply)