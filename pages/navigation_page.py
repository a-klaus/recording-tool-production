"""
Navigation page of the recording tool
"""

import os

import streamlit as st
from streamlit_mic_recorder import mic_recorder

from utils.paths import PAGE_PATHS, PAGE_DICT
from utils.utils import log_out, file_exists, get_audio_files


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


st.header("Startseite", divider=True)

st.write("Im Aufnahme-Tool findest du eine Seite für die Aufnahme von"\
         " vorgelesenen Sätzen sowie spontaner Sprache."\
         # "Außerdem gibt es einen Bereich"\
         # " für Transkription, in dem aufgeschrieben werden kann, was in den Audio-Dateien"\
         # " gesagt wird."\
         " Wenn Du eine Aufnahmeseite bereits verwendet hast, kannst Du auf \"Direkt"\
         " zur Seite\" klicken, um die Erklärung zu überspringen.")

st.divider()

def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output["bytes"]
        st.audio(audio_bytes)

# Set up recorder
st.write("Mikrofon-Test:")

mic_recorder(
    start_prompt="Aufnahme beginnen",
    stop_prompt="Aufnahme beenden + Anzeigen",
    just_once=True,
    format="wav",
    key='my_recorder',
    callback=callback
)

st.divider()

st.subheader("Satzaufnahme")

st.write("Teil des Datensets sind 400 Sätze und Wörter, die vorgelesen werden müssen.")

# Buttons for switching between items
left_column, right_column = st.columns(2)

with left_column:
    if st.button("Direkt zur Seite für die Satzaufnahme",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "sentence_recording.py"))

with right_column:
    if st.button("Zur Erklärung für die Satzaufnahme",
                 use_container_width=True):
        st.switch_page(os.path.join("pages", "sentence_recording_explanation1.py"))

# st.subheader("Bilbeschreibung")
#
# st.write("In diesem Bereich werden Sprecher*innen gebeten, zwei verschiedene Bilder zu beschreiben")
#
# # Buttons for switching between items
# left_column, right_column = st.columns(2)
#
# with left_column:
#     if st.button("Direkt zur Seite für die Bildbeschreibung",
#                  use_container_width=True):
#         st.switch_page(os.path.join("pages", "image_description.py"))
#
# with right_column:
#     if st.button("Zur Erklärung für die Bildbeschreibung",
#                  use_container_width=True):
#         st.switch_page(os.path.join("pages", "image_description_explanation1.py"))
#
# st.subheader("Offene Prompts")
#
# st.write("In diesem Bereich werden offene Fragen und Prompts angezeigt, die spontan beantwortet werden sollen.")
#
# # Buttons for switching between items
# left_column, right_column = st.columns(2)
#
# with left_column:
#     if st.button("Direkt zur Seite für offene Prompts",
#                  use_container_width=True):
#         st.switch_page(os.path.join("pages", "prompt_free_speech.py"))
#
# with right_column:
#     if st.button("Zur Erklärung für die offenen Prompts",
#                  use_container_width=True):
#         st.switch_page(os.path.join("pages", "prompt_explanation1.py"))
#
#
# st.subheader("Transkription")
#
# st.write("Die Spontansprache, die bei der Bildbeschreibung und bei den offenen Prompts"\
#          " gesammelt wird, muss"\
#          " transkribiert werden. Das bedeutet, dass aufgeschrieben werden muss, was gesagt"\
#          " wurde. In diesem Tool können die Aufnahmen angehört und das Gesagte"\
#          " aufgeschrieben werden.")
#
#
# if st.session_state.transcription_locked:
#     st.badge("Es sind noch keine Audiodateien zur Transkription vorhanden",
#              icon=":material/warning:",
#              color="orange")
# else:
#     # Buttons for switching between items
#     left_column, right_column = st.columns(2)
#
#     with left_column:
#         if st.button("Direkt zur Seite für die Transkription",
#                      use_container_width=True):
#             st.switch_page(os.path.join("pages", "transcription.py"))
#
#     with right_column:
#         if st.button("Zur Erklärung für die Transkription",
#                      use_container_width=True):
#             st.switch_page(os.path.join("pages", "transcription_explanation1.py"))

