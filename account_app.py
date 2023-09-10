
import streamlit as st
import authanticated_run as app_run

# Define a session state object
class SessionState:
    def __init__(self):
        self.logged_in = False

# Initialize the session state
session_state = SessionState()

# Create a login page
def login_page():
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
            session_state.logged_in = True
            st.write('Good Job !!')
# Function to logout
def logout():
    session_state.logged_in = False

def main():
    if not session_state.logged_in:
        login_page()
    else:
        # st.sidebar.button("Logout", on_click=logout)
        app_run.main()

if __name__ == "__main__":
    main()