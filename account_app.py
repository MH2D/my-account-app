import streamlit as st
from st_files_connection import FilesConnection
from google.cloud import storage
from pathlib import Path
import sqlite3

# Your service account key information as a dictionary
service_account_info = {
    "type": st.secrets.connections.gcs.type,
    "project_id": st.secrets.connections.gcs.project_id,
    "private_key_id": st.secrets.connections.gcs.private_key_id,
    "private_key": st.secrets.connections.gcs.private_key,
    "client_email": st.secrets.connections.gcs.client_email,
    "client_id": st.secrets.connections.gcs.client_id,
    "auth_uri": st.secrets.connections.gcs.auth_uri,
    "token_uri": st.secrets.connections.gcs.token_uri,
    "auth_provider_x509_cert_url": st.secrets.connections.gcs.auth_provider_x509_cert_url,
    "client_x509_cert_url": st.secrets.connections.gcs.client_x509_cert_url
}

# Initialize a client with your service account info
CLIENT = storage.Client.from_service_account_info(service_account_info)
DATA_PATH = Path('data')
DB_NAME = 'account_management_test_2.db'

# Replace these with your values
bucket_name = "data-account-app"

# Get the bucket
bucket = CLIENT.get_bucket(bucket_name)

# Get the blob (object) corresponding to the SQLite database file
blob = bucket.blob(DB_NAME)

# Download the SQLite database file as bytes
db_file_bytes = blob.download_as_bytes()

# Open the SQLite database in memory (you can also specify a local file path)
CONN = sqlite3.connect(':memory:')
CURSOR = CONN.cursor()

# Execute a query to get all table names
CURSOR.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all the table names using fetchall()
tables = CURSOR.fetchall()
st.write(tables)

