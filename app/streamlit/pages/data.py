import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sqlite3
from app.data.db import connect_database
from app.data.datasets import get_all_data

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("You must log in to access this page.")
    st.stop()  # stops the rest of the page from loading

st.set_page_config(page_title="Data Science Analysis", page_icon="🛡️", layout="wide")

st.title("Data Science Analysis")



# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["📊 Analytics", "🔍 Insert,Update or Delete incidents" , "⚙️ Ask Questions"])

with tab1:
    conn = connect_database()
    # Load DataFrame from database
    df = get_all_data(conn)

    df['last_updated'] = pd.to_datetime(df['last_updated'], format="%Y-%m-%d",errors='coerce')
    df['hour'] = df['last_updated'].dt.hour
    fig = px.histogram(df, x='hour', nbins=24, title="Dataset last updated Time (Hour of Day)")
    st.plotly_chart(fig)


    st.sidebar.header("Filters")

    source_filter = st.sidebar.multiselect(
    "Data Source",
    options=df["source"].dropna().unique(),
    default=df["source"].dropna().unique(),
   )

    category_filter = st.sidebar.multiselect(
    "Category",
    options=df["category"].dropna().unique(),
    default=df["category"].dropna().unique(),
   )

    # Apply filters
    filtered_df = df[
    (df["source"].isin(source_filter)) &
    (df["category"].isin(category_filter))
    ]


    col1, col2 = st.columns(2)


# CHART 1: Incidents by Priority

    with col1:
        st.subheader("📊 Incidents by category")
        fig_cat= px.bar(
        filtered_df,
        x="category",
        title="Incidents by Category",
        color="severity"
    )
    st.plotly_chart(fig_cat, use_container_width=True)


# CHART 2: Incidents by Source

    with col2:
      st.subheader("🟢 Incidents by Source")
      fig = px.pie(df, names='source', title="Dataset Sources")
      st.plotly_chart(fig)

    

# CHART 3: Incidents by Hour of Day

    st.subheader("⏱️ Incidents by Hour of Day")
    fig_hour = px.bar(filtered_df, x="hour",title="Updated Incidents by Hour",)
    st.plotly_chart(fig_hour, use_container_width=True)

    fig = px.scatter(df, x='record_count', y='file_size_mb',color='category', title="Record Count vs File Size")
    st.plotly_chart(fig)
   

    grouped = df.groupby('category')['record_count'].mean().reset_index()
    fig = px.bar(grouped, x='category', y='record_count',title="Average Record Count per Category")
    st.plotly_chart(fig)

    fig = px.box(df, x='category', y='file_size_mb',
             title="File Size Distribution by Category")
    st.plotly_chart(fig)




# RAW DATA DISPLAY

    with st.expander("📄 View Raw Data"):
     st.dataframe(filtered_df)



    
with tab2:
      if st.button("Go to Data Record Update Page"):
         st.switch_page("pages/data2.py")

    
     
with tab3:
    if st.button("Go to Data Science Chatbot"):
      st.switch_page("pages/Data_Chatbot.py")


