"""
Login page of the recording tool
"""

import streamlit as st

from utils.utils import log_in


if not "login_hint" in st.session_state:
    st.session_state.login_hint = ""


st.header("DYSTINCT Aufnahme-Interface")

st.write("Herzlich Willkommen zur Datenerhebung für das DYSTINCT-Datenset für dysarthrische Sprache!")

st.write('Vielen Dank, dass du dich entschieden hast, an der Datensammlung für' \
         ' das DYSTINCT-Projekt mitzuwirken.'
         ' Gib im Feld Nutzer-ID die zugewiesene Nutzer-ID ein und klicke dann auf "Log in".')

user_id = ""

with st.form("user_login"):
    user_id = st.text_input("Nutzer-ID", placeholder=st.session_state.login_hint)
    st.form_submit_button("Log in")


if user_id:
    log_in(user_id)

