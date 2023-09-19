import pandas as pd
import streamlit as st
from PIL import Image
from urllib.request import urlopen
import pickle
import streamlit_authenticator as stauth
from pathlib import Path
from datetime import datetime
from datetime import timedelta
from datetime import date
import ssl
import pickle
from pathlib import Path
import base64
import io

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
    credentials, "cds_pack", "guW70qH9RX", cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    ssl._create_default_https_context = ssl._create_unverified_context

    imageLOGO = Image.open(urlopen("https://i.ibb.co/WGjVK32/logopng.png"))
    st.image(imageLOGO)
    st.title("ADV MTD Verifier")

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.markdown("---")
    uploaded_file = st.file_uploader(
        "Choose a file (Excel or CSV)", type=["xlsx", "csv"]
    )
    st.warning(
        """To get an accurate count of the number of devices shipped, 
           please edit your Excel or CSV file to include only the dates you want 
           to include in the count."""
    )

    code_map = {
        "1-6341-220": "QG-NON-AP",
        "1-6342-220": "QG-VIN-AP",
        "1-8411-10": "DaggerQG-TMo",
        "1-8421-10": "DaggerQG-TMo",
        "1-8423-210": "DaggerQG-TMo",
        "1-8431-10": "DaggerQG-TMo",
        "1-8411-20": "DaggerQG-AP",
        "1-8421-20": "DaggerQG-AP",
        "1-8423-220": "DaggerQG-AP",
        "1-8431-220": "DaggerQG-AP",
        "1-6341-10": "QG-NON-TMo",
        "1-6340-10": "QG-VIN-TMo",
        "1-6351-17": "QG-NON-VZW",
        "1-6350-17": "QG-VIN-VZW",
    }

    if uploaded_file is not None:
        file_name = uploaded_file.name
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, engine="python")
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.write("Error: Unsupported file type.")
        df = df.applymap(lambda x: x.replace('"', "") if isinstance(x, str) else x)
        df = df[~df["Code"].isin(["3-SHIP", "3-COD", "3-TAX", "9-2001", "9-DISC"])]
        df["Code"] = df["Code"].apply(lambda x: x[:-5] if x.count("-") == 3 else x)

        pivot = df.pivot_table(index="Code", values="Qty", aggfunc="sum")
        pivot = pivot.reset_index() # Reset the index to make "Code" a regular column
        if "Code" in pivot.columns:
            # Map the values of the "Code" column to their new values
            pivot["Code"] = pivot["Code"].map(code_map).fillna(pivot["Code"])
            # Group by the new "Code" column and sum the "Qty" values
            pivot = pivot.groupby("Code", as_index=False).sum()

            def download_excel(df):
                towrite = io.BytesIO()
                downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)
                towrite.seek(0)
                b64 = base64.b64encode(towrite.read()).decode()
                return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="result.xlsx">Download Results</a>'
            
            st.dataframe(pivot)
            st.markdown(download_excel(pivot), unsafe_allow_html=True)
        else:
            st.error("The 'Code' column is not present in the uploaded file.")
        
if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")
