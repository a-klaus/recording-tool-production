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

st.write("Ziel in der Bildbeschreibung ist es, möglichst viel und möglichst"\
         " spontane Sprache zu sammeln."\
         " Die Bilder sind deshalb detailreich gestaltet, sodass viele Aspekte"\
         " beschrieben werden können. Es können auch Ideen genannt werden, was"\
         " die Figuren auf den Bildern zueinander sagen oder im Anschluss an die"\
         " dargestellte Situation machen. Wichtig ist nur, dass der Sprecher oder"\
         " die Sprecherin die Aussagen über das Bild selbst formuliert.")

st.write("Bei der Aufnahme anwesende Personen können bei der Bildbeschreibung"\
         " mit Nachfragen helfen, wenn der Sprecher oder die Sprecherin"\
         " nicht weiter weiß, was zum gezeigten Bild noch gesagt werden kann."\
         " Es ist nicht schlimm, wenn in der Aufnahme damit ein kleines Gespräch"\
         " entsteht.")


# Buttons for switching between items
left_column, _, right_column = st.columns(3)

with left_column:
    if st.button("Vorherige Seite",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "image_description_explanation5.py"))

with right_column:
    if st.button("Zum Interface für Bildbeschreibung",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "image_description.py"))

