import streamlit as st
from st_files_connection import FilesConnection

# Establish a connection to Google Cloud Storage (GCS)
conn = st.experimental_connection("gcs", type=FilesConnection)
df = conn.read("data_ugo/ugo_expenses.csv", input_format="csv", ttl=600)

st.write('Que passo')
# conn.write('data_ugo/ugo_exp_2.csv', df)
st.write('trop biennnn')
st.write(st.secretsconnections.gcs.testing)