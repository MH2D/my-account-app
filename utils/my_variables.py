import streamlit as st
from pathlib import Path
from google.cloud import storage
import json 

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
BUCKET_NAME = "data-account-app"
USER_DEPENSES = 'ugo'
with open(DATA_PATH / 'categories.json', 'r') as json_file:
    CATEGORIES = json.load(json_file)
FRENCH_DATEFORMAT = "%Y-%m-%d"