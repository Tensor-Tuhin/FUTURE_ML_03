# FUTURE_ML_03
Customer Support Chatbot for Spotify (deployed using Streamlit)

A small rule‑based chatbot that answers common support questions for Spotify music app: app crashes, login issues, billing/subscription problems, offline mode, and a few simple FAQs. What it does-
- Reads each user message and matches keywords to decide the issue (crash, login, billing, etc.).
- Uses a tiny state dictionary to handle short multi‑turn flows, for example:
  “app keeps crashing” → bot asks for device/OS → bot suggests specific fixes.
  
Project structure-
- app.py         # decide_reply and bot_reply (core chatbot logic)
- deploy_app.py  # Streamlit UI that calls bot_reply
- requirements.txt # shared dependencies (includes Streamlit)
  
How it is deployed with Streamlit-
- deploy_app.py creates a chat UI with st.chat_message and st.chat_input.
- On every user message, it calls bot_reply(user_text,st.session_state) from app.py and shows the response in the browser.

Running the project- 
- pip install -r requirements.txt
- streamlit run deploy_app.py
