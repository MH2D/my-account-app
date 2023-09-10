import streamlit as st
from st_files_connection import FilesConnection
from google.cloud import storage
from pathlib import Path
import sqlite3
from io import BytesIO
import io
import csv
import pandas as pd

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
DB_NAME = 'ugo_expenses.csv'

# Replace these with your values
bucket_name = "data-account-app"

# Get the bucket
bucket = CLIENT.get_bucket(bucket_name)

# Get the blob (object) corresponding to the SQLite database file
blob = bucket.blob(DB_NAME)

# Read the CSV file directly into a DataFrame
content = blob.download_as_string()
df = pd.read_csv(BytesIO(content))
st.write(df)

# Convert the DataFrame to a CSV format
csv_content = df.to_csv(index=False)

# Define the blob (object) to write
blob = bucket.blob('test_saved.csv')

# Upload the CSV content to GCS
blob.upload_from_string(csv_content, content_type='text/csv')
st.write('saved')