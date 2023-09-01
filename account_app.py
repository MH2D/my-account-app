import streamlit as st
from st_files_connection import FilesConnection

# Create a GCS connection
conn = st.experimental_connection('gcs', type=FilesConnection)
t = conn.read(f"data-account-app/account_management_copy.db")

t 

print(t)