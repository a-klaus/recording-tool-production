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

st.write("Grundsätzlich sollten"\
         " die Prompts mit einigen spontanen Sätzen beantwortet werden."\
         " Dabei kann die Aufnahme laufen gelassen werden. Die Aufnahmen"\
         " können anschließend im Bereich für Transkription angehört und"\
         " transkribiert werden, d.h. es wird aufgeschrieben, was gesagt"\
         " wurde.")

# Buttons for switching between items
left_column, _, right_column = st.columns(3)

with left_column:
    if st.button("Vorherige Seite",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "prompt_explanation7.py"))

with right_column:
    if st.button("Zum Prompt-Interface",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "prompt_free_speech.py"))

