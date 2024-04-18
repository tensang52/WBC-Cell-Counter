
import streamlit as st
import streamlit_authenticator as stauth    
import pandas as pd
from datetime import date
from github_contents import GithubContents
import api_calls

def authenticate():
    """ Initialize the authentication status."""
    if 'credentials' not in st.session_state:
        login_df = pd.read_csv(LOGIN_FILE, index_col=0)
        credentials =  {'usernames':login_df.to_dict(orient="index")}
        st.session_state['credentials'] = credentials
    else:
        credentials = st.session_state['credentials']

    authenticator = stauth.Authenticate(credentials,cookie_name='login-cookie', cookie_key='')
    authenticator.login()

    if st.session_state["authentication_status"] is True:
        authenticator.logout()
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

