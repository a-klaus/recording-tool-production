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

st.write("In der Satzaufnahme müssen einzelne Sätze oder Wörter vorgelesen"\
         " oder nachgesprochen werden. Insgesamt gibt es 400 Sätze und Wörter.")

st.write("Die Aufnahmeoberfläche sieht so aus:")

st.image(os.path.join("media", "sentence_interface.jpg"))


# Buttons for switching between items
_, _, right_column = st.columns(3)

with right_column:
    if st.button("Nächste Seite",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "sentence_recording_explanation2.py"))


