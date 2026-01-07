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

st.write("Mittig auf der Seite wird das Item angezeigt, das eingesprochen werden"\
         " soll. Starte die Aufnahme, sprich das angezeigte Item ein"\
         " oder lass es durch den Sprecher oder die Sprecherin einsprechen,"\
         " und stoppe dann die Aufnahme. Diese wird automatisch gespeichert.")

st.image(os.path.join("media", "sentence_interface4.jpg"))

left_column, _, right_column = st.columns(3)


with left_column:
    if st.button("Vorherige Seite",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "sentence_recording_explanation3.py"))

with right_column:
    if st.button("Nächste Seite",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "sentence_recording_explanation5.py"))




