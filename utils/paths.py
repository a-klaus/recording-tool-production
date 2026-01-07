"""
Important path definitions.
"""

import os


IMAGE_DIR = "images"
LABEL_DIR = "labels"
PROMPT_DIR = "prompts"

PAGE_DICT = {
    os.path.join("pages", "navigation_page.py"): "Startseite",
    # ""os.path.join("pages", "explanation.py"),
    os.path.join("pages", "sentence_recording.py"): "Satzaufnahme",
    # os.path.join("pages", "image_description.py"): "Bildbeschreibung",
    # os.path.join("pages", "prompt_free_speech.py"): "Offene Fragen",
    # os.path.join("pages", "transcription.py"): "Transkription"
    # os.path.join("pages", "final_page.py"),
    # os.path.join("pages", "sentence_recording_explanation1.py"),
    # os.path.join("pages", "sentence_recording_explanation2.py"),
    # os.path.join("pages", "sentence_recording_explanation3.py"),
    # os.path.join("pages", "sentence_recording_explanation4.py"),
    # os.path.join("pages", "sentence_recording_explanation5.py"),
    # os.path.join("pages", "sentence_recording_explanation6.py"),
    # os.path.join("pages", "sentence_recording_explanation7.py"),
    # os.path.join("pages", "sentence_recording_explanation8.py")
}

PAGE_PATHS = list(PAGE_DICT.keys())

