import streamlit as st
import pandas as pd
import numpy as np
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
        st.switch_page("pages/1_Dashboard.py")  # path is relative to Home.py :contentReference[oaicite:1]{index=1}
    st.stop()  # Don’t show login/register again

tab_login, tab_register = st.tabs(["Login", "Register"])