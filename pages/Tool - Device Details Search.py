import pandas as pd
import streamlit as st
from PIL import Image
from urllib.request import urlopen
import pickle
import streamlit_authenticator as stauth
from pathlib import Path
from datetime import datetime
from datetime import date
import ssl
import pickle
from pathlib import Path
import base64
import os, psycopg2


current_dateTime = datetime.now()
start_dateTime = date(2022, 12, 1)

st.set_page_config(layout="wide")
# Hide 'Made with Streamlit' & app menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- USER AUTHENTICATION ---
names = ["", "", "", "", "", ""]
usernames = ["", "", "", "", "", ""]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {"usernames": {}}

for uname, name, pwd in zip(usernames, names, hashed_passwords):
    user_dict = {"name": name, "password": pwd}
    credentials["usernames"].update({uname: user_dict})

authenticator = stauth.Authenticate(
    credentials, "", "", cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    ssl._create_default_https_context = ssl._create_unverified_context

    imageLOGO = Image.open(urlopen("https://i.ibb.co/WGjVK32/logopng.png"))
    st.image(imageLOGO)
    st.title("Device Details Search")
    st.warning(
        "The uploaded file must be a CSV file and have a 'serial' header."
    )

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    DATABASE_URL = os.environ["DATABASE_URL"]
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")

    table = ["daggerqg", "arrowqg"]
    tables = st.sidebar.selectbox("Please select your device type: ", table)

    query = f"SELECT * FROM {tables}"
    device_serials = pd.read_sql(query, con=conn)

    serials = st.file_uploader("Choose a file (Excel or CSV)", type=["xlsx", "csv"])

    if serials is not None:
        uploaded_serials = pd.read_csv(serials)

        uploaded_serials["serial"] = uploaded_serials["serial"].astype(str).str.strip()
        device_serials["serial"] = device_serials["serial"].astype(str).str.strip()

        matches = uploaded_serials[
            uploaded_serials["serial"].isin(device_serials["serial"])
        ]

        if not matches.empty:
            matched_details = pd.merge(matches, device_serials, on="serial", how="left")

            csv_string = matched_details.to_csv(
                index=False, header=False, quoting=1, quotechar="'"
            )
            csv_string = "\n".join(
                [f"'{row.strip()}'," for row in csv_string.split("\n") if row.strip()]
            )
            csv_string = csv_string[:-1]

            csv_file = csv_string.encode()
            b64 = base64.b64encode(csv_file).decode()
            href = f'<a href="data:text/csv;base64,{b64}" download="matched_details.csv">Download matched details</a>'
            st.markdown(href, unsafe_allow_html=True)

            st.write(matched_details)
        else:
            st.write("No matching devices found.")


if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")
