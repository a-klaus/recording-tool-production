"""
Explanation page of the recording tool.
"""

import os
import re

import streamlit as st
from streamlit_mic_recorder import mic_recorder

from utils.utils import log_out, file_exists, read_text


with st.sidebar:
    st.button("Log out", on_click=log_out)
    if st.button("Zur Navigation"):
        st.switch_page(os.path.join("pages", "navigation_page.py"))


st.header("Tutorial", divider=True)
st.write(read_text(os.path.join("media", "intro_expl.txt")))

st.subheader("Navigation")
st.write(read_text(os.path.join("media", "expl2_nav.txt")))

st.subheader("Sätze vorlesen")
st.write(read_text(os.path.join("media", "expl3_sent.txt")))

st.divider()
# st.html("<center><h1>Dies ist ein Test.</h1></center>")
st.header('"Dies ist ein Test."')

st.divider()

# Audio demo

def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output["bytes"]
        st.audio(audio_bytes)

# Set up recorder
mic_recorder(
    start_prompt="Aufnahme beginnen",
    stop_prompt="Aufnahme beenden + Anzeigen",
    just_once=True,
    format="wav",
    key='my_recorder',
    callback=callback
)

st.write(read_text(os.path.join("media", "expl3_sent2.txt")))

st.subheader("Ein Bild beschreiben")
st.write(read_text(os.path.join("media", "expl4_image.txt")))

if st.button("Zurück zur Navigation"):
    st.switch_page(os.path.join("pages", "navigation_page.py"))


# TODO interaktives tutorial mit ton test
# if st.button("Tutorial starten"):
#     st.write("ok!")




# if st.button("Zum Interface für Satz-Aufnahme"):
#     missing_files = [
#         c for c, f in enumerate(st.session_state.filenames)
#          if not file_exists(st.session_state.output_dir, f)
#     ]
#     if missing_files:
#         st.session_state.item_index = missing_files[0]
#     else:
#         st.session_state.item_index = 0
#     st.switch_page(os.path.join("pages", "sentence_recording.py"))
#
# if st.button("Zum Interface für Bildbeschreibung"):
#     st.switch_page(os.path.join("pages", "image_description.py"))

