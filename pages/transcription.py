"""
Transcription interface
"""

import json
import os

import streamlit as st

from utils.paths import PAGE_PATHS, PAGE_DICT
from utils.utils import log_out


def update_index_audio(current, modif):
    """Update the spontaneous speech audio file index."""
    st.session_state.spont_index = current + modif

def transcribe(index):
    try:
        st.audio(st.session_state.spont_file_dict[index]["path"])
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.write(f'Fehler: Datei nicht gefunden.')
        return
    # Transcription Interface
    if st.session_state.spont_file_dict[index]["done"]:
        st.write("Transkription vorhanden")
        if st.button("Nochmal bearbeiten"):
            st.session_state.spont_file_dict[index]["done"] = 0
            # st.rerun()
    else:
        with st.form("transcription_interface"):
            transcription = st.text_area(
                "Was wird gesagt?",
                value=st.session_state.spont_file_dict[index]["text"],
                placeholder="Transkription eingeben"
            )
            mark_as_finished = st.checkbox("Als fertig markieren")
            save = st.form_submit_button("Speichern")
            if save:
                if mark_as_finished:
                    # TODO right now this is stackable
                    # if not st.session_state.spont_file_dict[index]["display"].endwwith(" ✓"):
                        # st.session_state.spont_file_dict[index]["display"] += " ✓"
                    st.session_state.spont_file_dict[index]["done"] = 1
                st.session_state.spont_file_dict[index]["text"] = transcription
                with open(st.session_state.transcription_dict_path, "w", encoding="utf-8") as file_out:
                    json.dump(st.session_state.spont_file_dict, file_out, ensure_ascii=False, indent=4)
                st.rerun()
                # TODO this switch does not work yet

def format_selectbox(index):
    item_name = st.session_state.spont_file_dict[index]["item"]
    if st.session_state.spont_file_dict[index]["done"]:
        current_status = " - Fertig"
    elif st.session_state.spont_file_dict[index]["text"]:
        current_status = " - In Bearbeitung"
    else:
        current_status = ""
    return f"Datei {index} \"{item_name}\"{current_status}"


# Initialize import variables
if not "spont_index" in st.session_state:
    st.session_state.spont_index = 1

# if not "transcription_dict_path" in st.session_state:
#     st.session_state.transcription_dict_path = os.path.join(st.session_state.output_dir, "transcription_dict.json")
#
# if not "spont_file_dict" in st.session_state:
#     if os.path.isfile(st.session_state.transcription_dict_path):
#         # Read data from file
#         with open(st.session_state.transcription_dict_path, encoding="utf-8") as file_in:
#             st.session_state.spont_file_dict = {int(k): v for k, v in json.loads(file_in.read()).items()}
#     else:
#         # Create new dict
#         audio_files = get_audio_files(st.session_state.output_dir)
#         st.session_state.spont_file_dict = {
#             c+1: {"path": filename, "done": 0, "text": ""}
#             for c, filename in enumerate(audio_files)
#         }


with st.sidebar:
    st.button("Log out", on_click=log_out)
    st.divider()
    page_selection = st.selectbox(
        "Zu Seite wechseln",
        PAGE_PATHS,
        format_func=lambda x: PAGE_DICT[x]
    )
    if st.button("Auswählen"):
        st.switch_page(page_selection)
    st.divider()

    # Selectbox to jump to specific sentence
    start_item = st.selectbox(
        "Zu Satz springen:",
        # [i["display"] for i in st.session_state.spont_file_dict.values()],
        list(st.session_state.spont_file_dict.keys()),
        format_func=format_selectbox,
        # TODO maybe switch away from filenames
        index=st.session_state.spont_index - 1
    )
    if st.button("Item auswählen"):
        st.session_state.spont_index = start_item

st.header("Transkription")

st.divider()


if st.session_state.spont_file_dict:
    st.write(st.session_state.spont_file_dict[st.session_state.spont_index]["path"])
    transcribe(st.session_state.spont_index)

    # Buttons for switching between items
    left_column, right_column = st.columns(2)

    with left_column:
        if st.session_state.spont_index == 1:
            # Display button to get back to explanation
            if st.button("Zurück zur Navigation",
                      key="navigation",
                      type="tertiary",
                      use_container_width=True):
                st.switch_page(os.path.join("pages", "navigation_page.py"))
        else:
            # Display button to get back to previous sentence
            st.button(
                "Vorherige Aufnahme",
                key="backward",
                on_click=update_index_audio,
                args=(st.session_state.spont_index, -1),
                type="secondary",
                use_container_width=True
            )

    with right_column:
        if st.session_state.spont_index == len(st.session_state.spont_file_dict):
            # Display button to get to final page
            if st.button("Transkription beenden",
                      key="quit_transcription",
                      type="tertiary",
                      use_container_width=True):
                st.switch_page(os.path.join("pages", "final_page.py"))
        else:
            # Display button to get to next sentence
            st.button(
                "Nächste Aufnahme",
                key="forward",
                on_click=update_index_audio,
                args=(st.session_state.spont_index, +1),
                type="secondary",
                use_container_width=True
            )

else:
    st.write("Nothing recorded yet")

