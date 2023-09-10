
import streamlit as st

username = st.text_input("Username", value="")

pwd = st.text_input("Password", value="", type="password")

try:
    st.write(st.secrets[username])
except:
    st.error('Wrong username', icon="🚨")