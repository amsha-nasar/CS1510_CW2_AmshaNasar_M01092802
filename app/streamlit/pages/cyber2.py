
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
from app.data.incidents import insert_incident, get_all_incidents,update_incident_status,delete_incident,get_incidents_by_type_count,get_high_severity_by_status

conn = connect_database()
df = get_all_incidents(conn)

st.set_page_config(page_title="Cybersecurity Record Alteration", page_icon="🛡️", layout="wide")
st.title("Altering Records")

st.subheader("🟢 Insert Incidents")
if st.button("Add new incident"):

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
if st.button("Update incident"):
        
         update_id=st.text_input("Enter incident ID to update", key="update_id")
         new_status=st.selectbox("Enter new status", ["Open", "Investigating", "Resolved", "Closed"], key="new_status")

if st.button("Update"):
          records=update_incident_status(conn,update_id,new_status)
          if records==0:
              st.warning(f"No records were updated.")
          else:
              st.success(f"{records} records updated successfully.")
          


st.subheader("🟢 Delete Incidents")
if st.button("Delete incident"):
         delete_id=st.text_input("Enter incident ID to delete", key="delete_id")

if st.button("Delete"):
    records=delete_incident(conn,delete_id)
    if records==0:
        st.warning(f"No records were deleted.")
    else:
        st.success(f"{records} records deleted successfully.")