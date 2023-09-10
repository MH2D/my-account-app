import streamlit as st
import sqlite3
import json
from pathlib import Path
import pandas as pd
import plotly.graph_objs as go
import colorsys
import seaborn as sns
import numpy as np
from google.cloud import storage
from io import BytesIO

DB_NAME = "wtf"
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

def read_csv_from_gcs(csv_filename, bucket_name=BUCKET_NAME):
    # Get the bucket
    bucket = CLIENT.get_bucket(bucket_name)

    # Get the blob (object) corresponding to the SQLite database file
    blob = bucket.blob(csv_filename)

    # Read the CSV file directly into a DataFrame
    content = blob.download_as_string()
    csv_df = pd.read_csv(BytesIO(content))

    return csv_df

def write_csv_to_gcs(to_save_df, saved_filename, bucket_name=BUCKET_NAME):
    
    csv_content = to_save_df.to_csv(index=False)
    
    # Define the blob (object) to write
    bucket = CLIENT.get_bucket(bucket_name)

    # Define the blob (object) to write
    blob = bucket.blob(saved_filename)

    # Upload the CSV content to GCS
    blob.upload_from_string(csv_content, content_type='text/csv')


# Convert RGB tuple to hexadecimal color code
def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    #Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [(x+1)/(n+1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]

def callback():
    st.session_state.button_clicked = True