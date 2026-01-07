"""
Some functions needed.
"""

import json
import os
import re

import streamlit as st

from utils.paths import LABEL_DIR, PROMPT_DIR


# Log in, log out
def setup_sentence_recording_variables():
    st.session_state.sentence_items = load_labels(LABEL_DIR)
    st.session_state.prompt_items = load_labels(PROMPT_DIR)
    st.session_state.item_index = 0
    for c, item in st.session_state.sentence_items.items():
        if not item["done"]:
            st.session_state.item_index = c
            break

    # Initialize import variables
    if not "item_index" in st.session_state:
        st.session_state.item_index = 0

    if not "final_items" in st.session_state:
        st.session_state.final_items = len(st.session_state.sentence_items) - 1

def setup_spont_recording_variables():
    # Sort out state vars
    st.session_state.prompt_index = 0
    for c, item in st.session_state.prompt_items.items():
        if not item["done"]:
            st.session_state.prompt_index = c
            break

    # Initialize import variables
    if not "prompt_index" in st.session_state:
        st.session_state.prompt_index = 0

    if not "prompt_final_items" in st.session_state:
        st.session_state.prompt_final_items = len(st.session_state.prompt_items) - 1

    if not "spont_file_indices" in st.session_state:
        audio_id_dict = {k.split(".")[0]: 0 for k in os.listdir("images") + os.listdir("prompts")}
        for i in st.session_state.spont_file_dict.values():
            filename_split = os.path.split(i["path"])[1].split("_")
            item_name = filename_split[0]
            audio_id = int(filename_split[1])
            if audio_id_dict[item_name] < audio_id:
                audio_id_dict[item_name] = audio_id
        st.session_state.spont_file_indices = audio_id_dict

def setup_transcription_recording_variables():
    # Sort out state vars
    # if not "transcription_dict_path" in st.session_state:
    st.session_state.transcription_dict_path = os.path.join(st.session_state.output_dir, "transcription_dict.json")

    if os.path.isfile(st.session_state.transcription_dict_path):
        st.session_state.transcription_locked = False
        # Read data from file
        with open(st.session_state.transcription_dict_path, encoding="utf-8") as file_in:
            st.session_state.spont_file_dict = {int(k): v for k, v in json.loads(file_in.read()).items()}
        st.session_state.spont_file_index = max(st.session_state.spont_file_dict.keys())
    else:
        # Create new dict
        st.session_state.transcription_locked = True
        st.session_state.spont_file_dict = {}
        st.session_state.spont_file_index = 1
        # else:
        #     # Create new dict
        #     st.session_state.spont_file_dict = {
        #         c+1: {"path": filename, "done": 0, "text": ""}
        #         for c, filename in enumerate(audio_files)
        #     }
        #
        #     missing_audio_files = set(audio_files) - {v["path"] for v in st.session_state.spont_file_dict.values()}
        #     final_item = sorted(list(st.session_state.spont_file_dict.keys()))[-1]
        #     c_range = range(final_item, final_item + len(missing_audio_files))
        #     for c, filename in zip(c_range, missing_audio_files):
        #         st.session_state.spont_file_dict[c+1] = {"path": filename, "done": 0, "text": ""} 


def log_in(user_id):
    """Generic login check"""
    if user_id:
        os.makedirs(f"{user_id}_recordings", exist_ok=True)
        st.session_state.output_dir = f"{user_id}_recordings"
        # Get items from folder
        setup_sentence_recording_variables()
        setup_transcription_recording_variables()
        setup_spont_recording_variables()

        st.session_state.logged_in = True
        st.rerun()
    else:
        st.session_state.login_hint = "Hier Nutzer-ID eingeben!"
        st.rerun()

def log_out():
    st.session_state.logged_in = False

# Load data

# @st.cache_data
def load_labels(label_dir):
    """Load labels saved in label directory.

    Args:
        label_dir (str): path to directory containing the labels as .txt files

    Returns:
        items (list[str]): list of sentences to be read by the participant
        filenames (list[str]): parallel list of filenames
    """
    filenames = list(sorted(os.listdir(label_dir)))
    # Read in files
    items = {}
    for c, filename in enumerate(filenames):
        with open(os.path.join(label_dir, filename), encoding="utf-8") as file_in:
            exists = int(file_exists(st.session_state.output_dir, filename))
            items[c] = {"filename": filename, "text": file_in.read(), "done": exists}
    return items

def read_text(filepath):
    with open(filepath, encoding="utf-8") as file_in:
        lines = [line.strip() for line in file_in]
        text = " ".join(lines)
        text = re.sub(" +", " ", text)
    return text

def display_image(image_path, output_dir):
    image_name = image_path.split(".")[0]
    st.session_state.image = image_path

# Navigate through items

def file_exists(output_dir, filename):
    """Check if file exists in directory"""
    # TODO I think there is a more pythonic way to do this
    files = set(os.listdir(output_dir))
    return filename.replace(".txt", ".wav") in files

def get_audio_files(recording_dir):
    """Load spontaneous speech audio.

    Args:
        recording_dir (str): path to directory containing the audio files

    Returns:
        audios (list[str]): the audio file_names
    """
    audio_files = [
        os.path.join(recording_dir, i) for i in sorted(os.listdir(recording_dir))
        if i.endswith("_spont.wav")
    ]
    return audio_files


# Save audio

def update_transcription_dict(file_out_name, item):
    # Update prompt related state variables
    st.session_state.transcription_locked = False
    st.session_state.spont_file_dict[st.session_state.spont_file_index] = {
        "path": file_out_name,
        "done": 0,
        "item": item,
        "text": ""
    }
    st.session_state.spont_file_index += 1
    with open(st.session_state.transcription_dict_path, "w", encoding="utf-8") as file_out:
        json.dump(st.session_state.spont_file_dict, file_out, ensure_ascii=False, indent=4)
    # TODO maybe change the structure again so we can just append here?

def save_audio_spont(output_dir, item_file, audio):
    """Save audio to file.

    Args:
        output_dir (str): directory to save the audio files to
        filename (str): name of the original item .txt file
        audio (streamlit.runtime.uploaded_file_manager.UploadedFile'): audio
            as recorded via the streamlit interface
    """
    # Derive output filename from original .txt
    file_out_name = item_file
    st.session_state.spont_file_indices[file_out_name] += 1
    audio_id = str(st.session_state.spont_file_indices[file_out_name])
    file_out_name = f"{file_out_name}_{audio_id}_spont.wav"
    file_out_name = os.path.join(output_dir, file_out_name)
    # Save audio to file
    with open(file_out_name, "wb") as file_out:
        file_out.write(audio)
    update_transcription_dict(file_out_name, item_file.split(".")[0])

def save_audio_sent(output_dir, filename, audio_bytes):
    file_out_name = filename.replace(".txt", ".wav")
    file_out_name = os.path.join(output_dir, file_out_name)
    # Save audio to file
    with open(file_out_name, "wb") as file_out:
        file_out.write(audio_bytes)

