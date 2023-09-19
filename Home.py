import pandas as pd
import streamlit as st
from PIL import Image
from urllib.request import urlopen
from datetime import datetime
from datetime import date
from datetime import date
import ssl
import pickle
import streamlit_authenticator as stauth
from pathlib import Path

current_dateTime = datetime.now()
start_dateTime = date(2022, 12, 1)

st.set_page_config(
    page_title="Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

# --- USER AUTHENTICATION ---
names = ["name1, "name2", "name3"]

usernames = ["username1", "username2", "username3"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {"usernames": {}}

for uname, name, pwd in zip(usernames, names, hashed_passwords):
    user_dict = {"name": name, "password": pwd}
    credentials["usernames"].update({uname: user_dict})

authenticator = stauth.Authenticate(
    credentials, "any", "random", cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    # Hide 'Made with Streamlit' & app menu
    hide_streamlit_style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    imageLOGO = Image.open(urlopen("https://i.ibb.co/WGjVK32/logopng.png"))
    st.image(imageLOGO)
    st.header("Dashboard")

    st.header("")
    authenticator.logout("Signout", "sidebar")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        image_url = ""
        link_url = ""
        st.markdown(
            f'<a href="{link_url}"><img src="{image_url}" alt="image"></a>',
            unsafe_allow_html=True,
        )

    with col2:
        image_url = ""
        link_url = ""
        st.markdown(
            f'<a href="{link_url}"><img src="{image_url}" alt="image"></a>',
            unsafe_allow_html=True,
        )

    with col3:
        image_url = ""
        link_url = ""
        st.markdown(
            f'<a href="{link_url}"><img src="{image_url}" alt="image"></a>',
            unsafe_allow_html=True,
        )

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")
