"""
A simple first version for a streamlit recording tool for recording free speech
"""

import os
import streamlit as st

from streamlit_mic_recorder import mic_recorder

from utils.paths import IMAGE_DIR, PAGE_PATHS, PAGE_DICT
from utils.utils import (
    log_out,
    display_image,
    save_audio_spont,
    file_exists
)


image_paths = os.listdir(IMAGE_DIR)


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

    st.divider()
    # Selectbox to select image
    image_selection = st.selectbox(
        "Bild auswählen:",
        image_paths
    )
    image_path = os.path.join(IMAGE_DIR, image_selection)
    st.button("Item auswählen",
              on_click=display_image,
              args=(image_path, st.session_state.output_dir))
    st.divider()
    # Display audio
    display_audio = st.toggle("Letzte Aufnahmen anzeigen", value=False)

def callback():
    filename = os.path.split(st.session_state.image)[1].replace(".png", "")
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output["bytes"]
        save_audio_spont(st.session_state.output_dir, filename, audio_bytes)
        st.write(f"Aufnahme {str(st.session_state.spont_file_indices[filename])} gespeichert ✓")
        if display_audio:
            st.write("Letzte Aufnahme:")
            st.audio(audio_bytes)

if "image" in st.session_state:
    # Display image
    image_path = os.path.join(IMAGE_DIR, image_selection)
    st.image(st.session_state.image)
    # Set up recorder
    mic_recorder(
        start_prompt="Aufnahme beginnen",
        stop_prompt="AUFNAHME LÄUFT",
        just_once=True,
        format="wav",
        key='my_recorder',
        callback=callback
    )
else:
    image_selection = st.selectbox(
        "Bild auswählen:",
        image_paths
    )
    image_path = os.path.join(IMAGE_DIR, image_selection)
    st.button("Item auswählen",
              on_click=display_image,
              args=(image_path, st.session_state.output_dir))

