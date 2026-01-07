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


st.header("Transkription")

st.write("Transkriptionen können zeitaufwändig und schwierig sein."\
         " Manchmal ist nicht klar zu verstehen, was in der Aufnahme gesagt wurde."\
         " In solchen Fällen kann man dies in der Transkription mit entsprechenden"\
         " Markern anzeigen.")

st.write("Für gänzlich unverständliche Passagen kann [?]"\
         " verwendet werden.")
st.write("Beispiel: \"Dort ist ein [?] zu sehen.\"")

st.write("Wenn es eine Idee gibt, was in einer Passage gesagt"\
         " wird, dies aber unsicher ist, kann das ähnlich dargestellt werden:"\
         " [?Hypothese]")
st.write("Beispiel: \"Dort ist ein [?kleines Kind] zu sehen.\"")


# Buttons for switching between items
left_column, _, right_column = st.columns(3)

with left_column:
    if st.button("Vorherige Seite",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "transcription_explanation7.py"))

with right_column:
    if st.button("Zum Interface für Transkription",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "transcription.py"))

