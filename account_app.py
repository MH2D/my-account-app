import streamlit as st
from st_files_connection import FilesConnection

# Establish a connection to Google Cloud Storage (GCS)
conn = st.experimental_connection("gcs")

# Define the path to your SQLite3 .db file in GCS
db_file_path = "data-account-app/account_management_copy.db"

# Read the file using the connection
with conn.read(db_file_path) as file:
    # Perform actions with the file
    # For example, you can read its content or use it as a SQLite3 database
    file_content = file.read()