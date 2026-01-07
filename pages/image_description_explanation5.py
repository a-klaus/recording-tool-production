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


st.header("Bildbeschreibung")

st.write("Mit der Auswahl \"Letzte Aufnahme anzeigen\" kann die aufgenommene"\
         " Audiodatei angezeigt werden. In der Bildbeschreibung werden alle"\
         " Aufnahmen einzeln gespeichert, es wird also keine Datei überschrieben.")

st.write("Die Aufnahmen aus der Bildbeschreibung können anschließend in der"\
         " Oberfläche für Transkription transkribiert werden. Das bedeutet,"\
         " es wird aufgeschrieben, was in der Aufnahme gesagt wird.")

st.image(os.path.join("media", "image_interface6.jpg"))


# Buttons for switching between items
left_column, _, right_column = st.columns(3)

with left_column:
    if st.button("Vorherige Seite",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "image_description_explanation4.py"))

with right_column:
    if st.button("Nächste Seite",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "image_description_explanation6.py"))

