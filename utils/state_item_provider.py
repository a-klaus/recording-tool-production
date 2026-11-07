"""
Provides important things for the session state.
"""

import os
import yaml
from yaml.loader import SafeLoader

import streamlit as st
import streamlit_authenticator as stauth


def get_authenticator():
    with open('../config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Pre-hashing all plain text passwords once
    # stauth.Hasher.hash_passwords(config['credentials'])

    return stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )


class SentenceItems:
    """Gimme all da promps as a dict."""

    def __init__(self, user_id, prompt_dir):
        self.prompt_dir = prompt_dir
        self.out_dir = "../{user_id}_recordings"

        # Make sure data dir exists
        os.makedirs(self.out_dir, exist_ok=True)

        self.sentence_items = self.load_labels(self.prompt_dir)

    @staticmethod
    def file_exists(output_dir, filename):
        """Check if file exists in directory"""
        # TODO I think there is a more pythonic way to do this
        files = set(os.listdir(output_dir))
        return filename.replace(".txt", ".wav") in files

    def load_labels(self, label_dir):
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
                exists = int(self.file_exists(self.out_dir, filename))
                items[c] = {"filename": filename, "text": file_in.read(), "done": exists}
        return items

    def keys(self):
        return self.sentence_items.keys()

    def __getitem__(self, index):
        return self.sentence_items[index]

    def __len__(self):
        return len(self.sentence_items)

