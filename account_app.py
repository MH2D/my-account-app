
import streamlit as st
import authanticated_run as app_run
username = st.text_input("Username", value="")

pwd = st.text_input("Password", value="", type="password")

if st.button("Sign in"):
    try:
        secret_pwd = st.secrets[username].password
        if secret_pwd == pwd:
            error = False
        else:
            error = True
    except:
        error = True

    if error:      
        st.error('Wrong username or password', icon="🚨")
    else:
        app_run.main()