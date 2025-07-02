# tts.py

import streamlit as st

def speak_text(text):
    st.markdown(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{text}");
        window.speechSynthesis.speak(msg);
        </script>
    """, unsafe_allow_html=True)
