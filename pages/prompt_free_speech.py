"""
A simple first version for a streamlit recording tool for sentences
"""

import os
from time import sleep

import streamlit as st
from streamlit_mic_recorder import mic_recorder

from utils.paths import PAGE_PATHS, PAGE_DICT
from utils.utils import (
    save_audio_spont,
    file_exists,
    log_out,
)


### INTERFACE
def format_sentence_item(index):
    formatted_item = st.session_state.prompt_items[index]["filename"]
    if st.session_state.prompt_items[index]["done"]:
        formatted_item += " ✓"
    return formatted_item

def jump_to_item(start_item):
    st.session_state.prompt_index = start_item

def update_index(modif):
    st.session_state.prompt_index = st.session_state.prompt_index + modif

# Sidebar to allow jumping to specific item
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
    # Selectbox to jump to specific sentence
    start_item = st.selectbox(
        "Zu Prompt springen:",
        list(st.session_state.prompt_items.keys()),
        format_func=format_sentence_item,
        index=st.session_state.prompt_index
    )
    st.button("Item auswählen", on_click=jump_to_item, args=(start_item,))
    st.divider()
    # Auto-skip
    auto_skip = st.toggle("Automatisch zum nächsten Prompt wechseln", value=True)
    # Display audio
    display_audio = st.toggle("Vorhandene Aufnahmen anzeigen", value=False)

# Buttons for switching between items
left_column, right_column = st.columns(2)

with left_column:
    if st.session_state.prompt_index == 0:
        # Display button to get back to explanation
        if st.button("Zurück zur Navigation",
                  key="expl",
                  type="tertiary",
                  use_container_width=True):
            st.switch_page(os.path.join("pages", "navigation_page.py"))
    else:
        # Display button to get back to previous sentence
        st.button(
            "Vorheriger Prompt",
            key="backward",
            # on_click=update_index,
            # args=(st.session_state.item_list, -1, len(st.session_state.item_list)),
            on_click=update_index,
            args=(-1,),
            type="secondary",
            use_container_width=True
        )
# TODO make buttons work again

with right_column:
    if st.session_state.prompt_index == st.session_state.prompt_final_items:
        # Display button to get to final page
        if st.button("Aufnahmen beenden",
                  key="quit_rec",
                  type="tertiary",
                  use_container_width=True):
            st.switch_page(os.path.join("pages", "final_page.py"))
    else:
        # Display button to get to next sentence
        st.button(
            "Nächster Prompt",
            key="forward",
            # on_click=update_index,
            # args=(st.session_state.item_list, +1, len(st.session_state.item_list)),
            on_click=update_index,
            args=(+1,),
            type="secondary",
            use_container_width=True
        )

# Get audio input

def callback():
    filename = os.path.split(st.session_state.prompt_items[st.session_state.prompt_index]["filename"])[1].replace(".txt", "")
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output["bytes"]
        save_audio_spont(st.session_state.output_dir, filename, audio_bytes)
        st.session_state.prompt_items[st.session_state.prompt_index]["done"] = 1
        # Rerun to get to the next sentence
        if auto_skip:
            if st.session_state.prompt_index + 1 < len(st.session_state.prompt_items):
                st.session_state.prompt_index = st.session_state.prompt_index + 1
                st.rerun()
            else:
                st.switch_page(os.path.join("pages", "final_page.py"))

# Set up recorder
mic_recorder(
    start_prompt="Aufnahme beginnen",
    stop_prompt="AUFNAHME LÄUFT",
    just_once=True,
    format="wav",
    key='my_recorder',
    callback=callback
)

st.divider()

# Info about item:
st.write(f'Prompt {st.session_state.prompt_index + 1}/{st.session_state.prompt_final_items+1}{" - Aufnahme existiert" if st.session_state.prompt_items[st.session_state.prompt_index]["done"] else ""}')

# Display sentence to be read
st.header(f'{st.session_state.prompt_items[st.session_state.prompt_index]["text"]}')

st.divider()

# Optionally display existing audio
if display_audio:
    if file_exists(st.session_state.output_dir, st.session_state.prompt_items[st.session_state.prompt_index]["filename"]):
        st.audio(os.path.join(st.session_state.output_dir, st.session_state.prompt_items[st.session_state.prompt_index]["filename"].replace(".txt", ".wav")))

