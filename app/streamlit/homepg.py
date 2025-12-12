import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
import pandas as pd
import numpy as np
from app.services.user_service import login_user,register_user
#import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("Dashboard")

st.markdown("""
    <style>
    .stApp {
        background-color: #FFB6C1;
    }
    </style>
""", unsafe_allow_html=True)

if "users" not in st.session_state:
    # Very simple in-memory "database": {username: password}
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🔐 Welcome")

# If already logged in, go straight to dashboard (optional)
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard"):
        # Use the official navigation API to switch pages
        st.switch_page("pages/cyber.py")  
    st.stop()  

tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login")


    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        ok, result = login_user(username, password)
        if ok:
            st.session_state.logged_in = True
            st.session_state.user = result
            st.success(f"Welcome {username}!")
            if st.button("Go to cybersecurity dashboard"):
               st.switch_page("pages/cyber.py")
           
        else:
            st.error(result)
            # Redirect to dashboard page


with tab_register:   
    st.subheader("Register")

    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    role = st.selectbox("Select role", ["user", "admin"])

    if st.button("Register"):
        ok, result = register_user(username, password, role)
        if ok:
            st.success(result)
            st.info("You can now login")
        else:
            st.error(result)


