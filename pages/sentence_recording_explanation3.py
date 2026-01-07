"""
Tutorial for sentence recording.
"""

import os

import streamlit as st
from streamlit_mic_recorder import mic_recorder

from utils.paths import PAGE_PATHS, PAGE_DICT
from utils.utils import (
    log_out,
)


with st.sidebar:
    st.button("Log out", on_click=log_out)
    st.divider()
    page_selection = st.selectbox(
        "Zu Seite wechseln",
        [i for i in PAGE_PATHS if (not i.endswith("transcription.py")) or (not st.session_state.transcription_locked)],
        format_func=lambda x: PAGE_DICT[x]
    )
    if st.button("Auswählen"):
        st.switch_page(page_selection)


st.header("Satzaufnahme")

st.write("Unter den Knöpfen für den Itemwechsel ist der Aufnahmeknopf. Wird"\
         " dieser geklickt, startet die Aufnahme. Eventuell muss zunächst die"\
         " Audio-Aufnahme über den Browser erlaubt werden. Um die Aufnahme zu"\
         " stoppen, wird derselbe Knopf ein zweites Mal geklickt.")

st.image(os.path.join("media", "sentence_interface3.jpg"))

st.write("Hier kann die Aufnahme ausprobiert werden:")

def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output["bytes"]
        st.audio(audio_bytes)

mic_recorder(
    start_prompt="Aufnahme beginnen",
    stop_prompt="Aufnahme beenden + Anzeigen",
    just_once=True,
    format="wav",
    key='my_recorder',
    callback=callback
)


left_column, _, right_column = st.columns(3)


with left_column:
    if st.button("Vorherige Seite",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "sentence_recording_explanation2.py"))

with right_column:
    if st.button("Nächste Seite",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "sentence_recording_explanation4.py"))




