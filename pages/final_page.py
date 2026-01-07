"""
Final page of the recording tool
"""

import os
import streamlit as st

from utils.utils import log_out


with st.sidebar:
    st.button("Log out", on_click=log_out)


"Danke für Ihre Mitarbeit!"


if st.button("Zur Navigation"):
    st.switch_page(os.path.join("pages", "navigation_page.py"))

