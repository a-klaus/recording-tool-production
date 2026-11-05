"""
Final page of the recording tool
"""

import os
import streamlit as st


with st.sidebar:
    st.session_state.authenticator.logout()


"Danke für Ihre Mitarbeit!"


if st.button("Zur Navigation"):
    st.switch_page(os.path.join("pages", "navigation_page.py"))

