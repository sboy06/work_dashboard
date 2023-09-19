import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
from urllib.request import urlopen
import pickle
import streamlit_authenticator as stauth
from pathlib import Path
import ssl


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
    st.title("Packaging Count Import")
    st.warning(
        "Headers: Qty, Type, Name and must be a CSV file type."
    )
    def update_gsheet(sheet, column, value):
        cell = sheet.find(column)
        next_row = len(sheet.col_values(cell.col)) + 1
        sheet.update_cell(next_row, cell.col, value)

    def update_individual_gsheet(sheet, column, value):
        cell = sheet.find(column)
        next_row = len(sheet.col_values(cell.col)) + 1
        sheet.update_cell(next_row, cell.col, value)

    try:
        st.markdown("---")
        uploaded_file = st.file_uploader(
            "Choose a file (Excel or CSV)", type=["xlsx", "csv"]
        )

        if uploaded_file is not None:
            file_name = uploaded_file.name
            if file_name.endswith(".csv"):
                df = pd.read_csv(uploaded_file, engine="python")
            elif file_name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                st.write("Error: Unsupported file type.")

            if 'Qty' in df.columns and 'Type' in df.columns and 'Name' in df.columns:
                result_df = df.groupby(['Type', 'Name'])['Qty'].sum()
                st.write(result_df)

                # Google Sheets API setup
                scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                     "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

                creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
                client = gspread.authorize(creds)
                spreadsheet = client.open("Database")
                bulk_sheet = spreadsheet.worksheet("bulk")
                individual_sheet = spreadsheet.worksheet("individual")

                for index, row in result_df.reset_index().iterrows():
                    if row['Type'] == 'Bulk':
                        update_gsheet(bulk_sheet, row['Name'], row['Qty'])
                    elif row['Type'] == 'Individual':
                        update_individual_gsheet(individual_sheet, row['Name'], row['Qty'])

    except AttributeError:
        pass

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")