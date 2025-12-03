
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
from app.data.db import connect_database
from app.data.incidents import insert_incident, get_all_incidents,update_incident_status,delete_incident,get_incidents_by_type_count,get_high_severity_by_status

'''if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("You must log in to access this page.")
    st.stop()  # stops the rest of the page from loading
'''
st.set_page_config(page_title="Cybersecurity Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ Cybersecurity Threat Analysis")



# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["📊 Analytics", "🔍 Insert,Update or Delete incidents" , "⚙️ Ask Questions"])

with tab1:
    conn = connect_database()
    # Load DataFrame from database
    df = get_all_incidents(conn)

    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
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

# -----------------------------------
# CHART 2: Incidents by Status
# -----------------------------------
    with col2:
      st.subheader("🟢 Incidents by Status")
    fig_status = px.pie(
        filtered_df,
        names="status",
        hole=0.45,
        title="Incident Status Distribution"
    )
    st.plotly_chart(fig_status, use_container_width=True)

# -----------------------------------
# CHART 3: Incidents by Hour of Day
# -----------------------------------
    st.subheader("⏱️ Incidents by Hour of Day")
    fig_hour = px.bar(
    filtered_df,
    x="hour",
    title="Reported Incidents by Hour",
    )
    st.plotly_chart(fig_hour, use_container_width=True)

# -----------------------------------
# CHART 4: Incidents by Category
# -----------------------------------
    st.subheader("📂 Incidents by Category")
    fig_category = px.bar(
    filtered_df,
    x="incident_type",
    color="incident_type",
    title="Incidents by Category",
  )
    st.plotly_chart(fig_category, use_container_width=True)

# -----------------------------------
# CHART 5: Treemap of Descriptions
# -----------------------------------
    st.subheader("🗂️ Top Attack Themes (Descriptions)")
    fig_tree = px.treemap(
    filtered_df,
    path=["description"],
    title="Incident Descriptions Treemap",
  )
    st.plotly_chart(fig_tree, use_container_width=True)

# -----------------------------------
# RAW DATA DISPLAY
# -----------------------------------
    with st.expander("📄 View Raw Data"):
     st.dataframe(filtered_df)



    
with tab2:
      st.subheader("🟢 Insert Incidents")
     

      incident_type=st.text_input("enter incident type",key="category")
      status=st.selectbox("enter status,",["Open","Investigating","Resolved","Closed"],key="insert_status")
      severity=st.selectbox("enter severity type,",["Low","Medium","High","Critical"],key="severity")
      description=st.text_input("enter incident description",key="des")
      reported_by=st.text_input("enter incident description",key="report")
      date=st.text_input("enter incident description",key="date")
      created_at=st.text_input("enter incident description",key="time")

      if st.button("Insert"):
          
          new_id=insert_incident(conn,incident_type, severity, status, date, description, reported_by, created_at)
          st.success(f"{new_id} is id of record inserted successfully.")
 
      st.subheader("🟢 Update Incidents")
      
      update_id=st.text_input("Enter incident ID to update", key="update_id")
      new_status=st.selectbox("Enter new status", ["Open", "Investigating", "Resolved", "Closed"], key="new_status")
      if st.button("Update"):
          records=update_incident_status(conn,update_id,new_status)
          if records==0:
              st.warning(f"No records were updated.")
          else:
              st.success(f"{records} records updated successfully.")
          


      st.subheader("🟢 Delete Incidents")
      delete_id=st.text_input("Enter incident ID to delete", key="delete_id")

      if st.button("Delete"):
         
          records=delete_incident(conn,delete_id)
          if records==0:
              st.warning(f"No records were deleted.")
          else:
              st.success(f"{records} records deleted successfully.")
          

    
     

          





    