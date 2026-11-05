"""
A simple first version for a streamlit recording tool
"""

import os
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from utils.utils import log_in


with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

if not "authenticator" in st.session_state:
    st.session_state.authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )


# Login widget
try:
    st.session_state.authenticator.login()
except Exception as e:
    st.error(e)

# Greet user
if st.session_state.get('authentication_status'):
    log_in(st.session_state["username"])
    pg = st.navigation([st.Page(os.path.join("pages", "navigation_page.py")),
                        st.Page(os.path.join("pages", "explanation.py")),
                        st.Page(os.path.join("pages", "image_description.py")),
                        st.Page(os.path.join("pages", "sentence_recording.py")),
                        st.Page(os.path.join("pages", "transcription.py")),
                        st.Page(os.path.join("pages", "prompt_free_speech.py")),
                        st.Page(os.path.join("pages", "final_page.py")),
                        # st.Page(os.path.join("pages", "prompt_explanation1.py")),
                        # st.Page(os.path.join("pages", "prompt_explanation2.py")),
                        # st.Page(os.path.join("pages", "prompt_explanation3.py")),
                        # st.Page(os.path.join("pages", "prompt_explanation4.py")),
                        # st.Page(os.path.join("pages", "prompt_explanation5.py")),
                        # st.Page(os.path.join("pages", "prompt_explanation6.py")),
                        # st.Page(os.path.join("pages", "prompt_explanation7.py")),
                        # st.Page(os.path.join("pages", "prompt_explanation8.py")),
                        # st.Page(os.path.join("pages", "transcription_explanation1.py")),
                        # st.Page(os.path.join("pages", "transcription_explanation2.py")),
                        # st.Page(os.path.join("pages", "transcription_explanation3.py")),
                        # st.Page(os.path.join("pages", "transcription_explanation4.py")),
                        # st.Page(os.path.join("pages", "transcription_explanation5.py")),
                        # st.Page(os.path.join("pages", "transcription_explanation6.py")),
                        # st.Page(os.path.join("pages", "transcription_explanation7.py")),
                        # st.Page(os.path.join("pages", "transcription_explanation8.py")),
                        # st.Page(os.path.join("pages", "image_description_explanation1.py")),
                        # st.Page(os.path.join("pages", "image_description_explanation2.py")),
                        # st.Page(os.path.join("pages", "image_description_explanation3.py")),
                        # st.Page(os.path.join("pages", "image_description_explanation4.py")),
                        # st.Page(os.path.join("pages", "image_description_explanation5.py")),
                        # st.Page(os.path.join("pages", "image_description_explanation6.py")),
                        st.Page(os.path.join("pages", "sentence_recording_explanation1.py")),
                        st.Page(os.path.join("pages", "sentence_recording_explanation2.py")),
                        st.Page(os.path.join("pages", "sentence_recording_explanation3.py")),
                        st.Page(os.path.join("pages", "sentence_recording_explanation4.py")),
                        st.Page(os.path.join("pages", "sentence_recording_explanation5.py")),
                        st.Page(os.path.join("pages", "sentence_recording_explanation6.py")),
                        st.Page(os.path.join("pages", "sentence_recording_explanation7.py")),
                        st.Page(os.path.join("pages", "sentence_recording_explanation8.py")),
                        st.Page(os.path.join("pages", "sentence_recording_explanation9.py")),
                        st.Page(os.path.join("pages", "sentence_recording_explanation10.py"))],
                       position="hidden")
    pg.run()
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')

