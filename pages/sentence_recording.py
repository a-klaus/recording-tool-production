"""
A simple first version for a streamlit recording tool for sentences
"""

import os
from time import sleep

import streamlit as st
from streamlit_mic_recorder import mic_recorder

from utils.paths import PAGE_PATHS, PAGE_DICT
from utils.utils import (
    save_audio_sent,
    file_exists,
)


# Set up idx for session state
if "idx" not in st.session_state:
    x = 0
    while st.session_state.sentence_items[x]["done"]:
        x += 1
    st.session_state.idx = x


### INTERFACE

def format_sentence_item(index):
    formatted_item = st.session_state.sentence_items[index]["filename"]
    if st.session_state.sentence_items[index]["done"]:
        formatted_item += " ✓"
    return formatted_item

def callback():
    filename = st.session_state.sentence_items[st.session_state.idx]["filename"]
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output["bytes"]
        save_audio_sent(st.session_state.output_dir, filename, audio_bytes)
        st.session_state.sentence_items[st.session_state.idx]["done"] = 1
        # Rerun to get to the next sentence
        if auto_skip:
            if st.session_state.idx + 1 < len(st.session_state.sentence_items):
                st.session_state.idx = st.session_state.idx + 1
                st.rerun()
            else:
                st.switch_page(os.path.join("pages", "final_page.py"))


# Sidebar to allow jumping to specific item
with st.sidebar:
    st.session_state.authenticator.logout()
    st.divider()
    page_selection = st.selectbox(
        "Zu Seite wechseln",
        [i for i in PAGE_PATHS if (not i.endswith("transcription.py")) or (not st.session_state.transcription_locked)],
        format_func=lambda x: PAGE_DICT[x]
    )
    if st.button("Auswählen"):
        st.switch_page(page_selection)
    st.divider()
    # Selectbox to jump to specific sentence
    start_item = st.selectbox(
        "Zu Satz springen:",
        list(st.session_state.sentence_items.keys()),
        format_func=format_sentence_item,
        index=st.session_state.idx
    )
    if st.button("Item auswählen"):#, on_click=jump_to_item, args=(start_item,)):
        st.session_state.idx = start_item
        st.rerun()
    st.divider()
    # Auto-skip
    auto_skip = st.toggle("Automatisch zum nächsten Satz wechseln", value=True)
    # Display audio
    display_audio = st.toggle("Vorhandene Aufnahmen anzeigen", value=False)


left_column, right_column = st.columns(2)

with left_column:
    if st.session_state.idx == 0:
        if st.button("Zurück zur Startseite", key="expl", type="tertiary", use_container_width=True):
            st.switch_page(os.path.join("pages", "navigation_page.py"))
    else:
        if st.button("← Previous", type="secondary", use_container_width=True):
            st.session_state.idx -= 1
            st.rerun()

with right_column:
    if st.session_state.idx == len(st.session_state.sentence_items):
        if st.button("Aufnahmen beenden", key="quit_rec", type="tertiary", use_container_width=True):
            st.switch_page(os.path.join("pages", "final_page.py"))
    else:
        if st.button("Next →", type="secondary", use_container_width=True):
            st.session_state.idx += 1
            st.rerun()


# Set up recorder
mic_recorder(
    start_prompt="Aufnahme beginnen",
    stop_prompt="AUFNAHME LÄUFT",
    just_once=True,
    format="wav",
    key='my_recorder',
    callback=callback
)


# Display Sentence
st.divider()

# Info about item:
st.write(f'Satz {st.session_state.idx+1}/{st.session_state.final_items+1}{" - Aufnahme existiert" if st.session_state.sentence_items[st.session_state.idx]["done"] else ""}')

# Display sentence to be read
st.header(f'{st.session_state.sentence_items[st.session_state.idx]["text"]}')

st.divider()


# Optionally display existing audio
if display_audio:
    if file_exists(st.session_state.output_dir, st.session_state.sentence_items[st.session_state.item_index]["filename"]):
        st.audio(os.path.join(st.session_state.output_dir, st.session_state.sentence_items[st.session_state.item_index]["filename"].replace(".txt", ".wav")))

