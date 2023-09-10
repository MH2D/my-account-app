
import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
import authanticated_run as depense_app



with open('data/configs.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    depense_app.main()
    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')