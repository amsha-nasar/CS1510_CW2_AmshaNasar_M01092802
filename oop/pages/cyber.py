
import sys
from pathlib import Path


# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sqlite3
from oop.services.database_manager import DatabaseManager
from oop.models.incidents import IncidentManager,SecurityIncident



if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("You must log in to access this page.")
    st.stop()  # stops the rest of the page from loading

st.set_page_config(page_title="Cybersecurity Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ Cybersecurity Threat Analysis")



# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["📊 Analytics", "🔍 Insert,Update or Delete incidents" , "⚙️ Ask Questions"])

with tab1:
   
    db = DatabaseManager("DATA/intelligence_platform.db")
    db.connect()
    incident=IncidentManager()
    df=incident.get_all_incidents

    

    df['created_at'] = pd.to_datetime(df['created_at'], format="%Y-%m-%d",errors='coerce')

    df['hour'] = df['created_at'].dt.hour


    st.sidebar.header("Filters")

    priority_filter = st.sidebar.multiselect(
    "Priority",
    options=df["severity"].dropna().unique(),
    default=df["severity"].dropna().unique(),
    )

    status_filter = st.sidebar.multiselect(
    "Status",
    options=df["status"].dropna().unique(),
    default=df["status"].dropna().unique(),
   )

    category_filter = st.sidebar.multiselect(
    "Category",
    options=df["incident_type"].dropna().unique(),
    default=df["incident_type"].dropna().unique(),
   )

    # Apply filters
    filtered_df = df[
    (df["severity"].isin(priority_filter)) &
    (df["status"].isin(status_filter)) &
    (df["incident_type"].isin(category_filter))
    ]


    col1, col2 = st.columns(2)


# CHART 1: Incidents by Priority

    with col1:
        st.subheader("📊 Incidents by severity")
        fig_priority = px.bar(
        filtered_df,
        x="severity",
        title="Incidents by severity",
        color="severity"
    )
    st.plotly_chart(fig_priority, use_container_width=True)


# CHART 2: Incidents by Status

    with col2:
      st.subheader("🟢 Incidents by Status")
    fig_status = px.pie(
        filtered_df,
        names="status",
        hole=0.45,
        title="Incident Status Distribution"
    )
    st.plotly_chart(fig_status, use_container_width=True)



# CHART 4: Incidents by Category
    st.subheader("📂 Incidents by Category")
    fig_category = px.bar(
    filtered_df,
    x="incident_type",
    color="incident_type",
    title="Incidents by Category",
  )
    st.plotly_chart(fig_category, use_container_width=True)

# CHART 5: Treemap of Descriptions

    st.subheader("🗂️ Top Attack Themes (Descriptions)")
    fig_tree = px.treemap(
    filtered_df,
    path=["description"],
    title="Incident Descriptions Treemap",
  )
    st.plotly_chart(fig_tree, use_container_width=True)


# RAW DATA DISPLAY

    with st.expander("📄 View Raw Data"):
     st.dataframe(filtered_df)



    
with tab2:
       db = DatabaseManager("DATA/intelligence_platform.db")
       conn=db.connect()
       incident=IncidentManager()


st.subheader("🟢 Insert Incidents")
if st.button("Add new incident"):

        incident_type=st.text_input("enter incident type",key="category")
        status=st.selectbox("enter status,",["Open","Investigating","Resolved","Closed"],key="insert_status")
        severity=st.selectbox("enter severity type,",["Low","Medium","High","Critical"],key="severity")
        description=st.text_input("enter incident description",key="des")
        reported_by=st.text_input("Reported by",key="report")
        date=st.text_input("Date of incident",key="date")
        created_at=st.text_input("Record creation time (optional)",key="time")

if st.button("Insert"):
          
          new_id=incident.insert_incident(incident_type, severity, status, date, description, reported_by, created_at)
          st.success(f"{new_id} is id of record inserted successfully.")
 
st.subheader("🟢 Update Incidents")
if st.button("Update incident"):
        
         update_id=st.text_input("Enter incident ID to update", key="update_id")
         new_status=st.selectbox("Enter new status", ["Open", "Investigating", "Resolved", "Closed"], key="new_status")

if st.button("Update"):
          records=incident.update_incident_status(update_id,new_status)
          if records==0:
              st.warning(f"No records were updated.")
          else:
              st.success(f"{records} records updated successfully.")
          


st.subheader("🟢 Delete Incidents")
if st.button("Delete incident"):
         delete_id=st.text_input("Enter incident ID to delete", key="delete_id")

if st.button("Delete"):
    records=incident.delete_incident(delete_id)
    if records==0:
        st.warning(f"No records were deleted.")
    else:
        st.success(f"{records} records deleted successfully.")





     
with tab3:
    if st.button("Go to Cyber Chatbot"):
      st.switch_page("pages/Chatbot.py")



    #streamlit run app/streamlit/homepg.py