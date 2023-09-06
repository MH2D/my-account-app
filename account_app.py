import streamlit as st
from st_files_connection import FilesConnection

# # Establish a connection to Google Cloud Storage (GCS)
# conn = st.experimental_connection("gcs", type=FilesConnection)
# df = conn.read("data_ugo/ugo_expenses.csv", input_format="csv", ttl=600)

# st.write('Que passo')
# # conn.write('data_ugo/ugo_exp_2.csv', df)
# st.write('trop biennnn')
# st.write(st.secrets.connections.gcs.testing)

from google.cloud import storage

# Replace these with your values
project_id = st.secrets.connections.gcs.project_id
bucket_name = "data-account-app"
object_name = "account_management_copy.db"

# Initialize a client
client = storage.Client(project=project_id)

# Get the bucket
bucket = client.get_bucket(bucket_name)

# Get the blob (object)
blob = bucket.blob(object_name)

# Download the object's content as a string
content = blob.download_as_text()

# Print or process the content as needed
content