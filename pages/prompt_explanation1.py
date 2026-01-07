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


st.header("Offene Prompts")

st.write("Wie in der Bildbeschreibung soll bei den offenen Fragen und Prompts"\
         " spontane Sprache gesammelt werden."\
         " Die Oberfläche sieht so aus:")


st.image(os.path.join("media", "prompt_interface1.jpg"))


# Buttons for switching between items
_, _, right_column = st.columns(3)

with right_column:
    if st.button("Nächste Seite",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "prompt_explanation2.py"))

