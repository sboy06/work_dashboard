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
import io
import base64

st.set_page_config(layout="wide")
# Hide 'Made with Streamlit' & app menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Define a function to create the Excel template with headers
def create_template():
    template_df = pd.DataFrame(columns=["Date", "Brand", "Qty", "Code"])
    template_bytes = io.BytesIO()
    with pd.ExcelWriter(template_bytes, engine="xlsxwriter") as writer:
        template_df.to_excel(writer, sheet_name="Sheet1", index=False)
    return template_bytes.getvalue()


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
    st.title("CDS MTD Verifier")

    def dataframe_to_excel_download_link(df, filename):
        excel_bytes = io.BytesIO()
        with pd.ExcelWriter(excel_bytes, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)
        excel_bytes.seek(0)
        b64 = base64.b64encode(excel_bytes.read()).decode()
        return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'

    # Define the function that will process the uploaded file
    def process_file(file):
        # Read the file into a Pandas dataframe
        df = pd.read_excel(file) if file.name.endswith(".xlsx") else pd.read_csv(file)

        # Replace the specified codes with their corresponding names
        code_replacements = {
            "8-6343-520": "QG-NON-AP",
            "8-6345-520": "QG-NON-AP",
            "8-6347-520": "QG-NON-AP",
            "8-6331-520": "QG-NON-AP",
            "8-6349-520": "QG-NON-AP",
            "8-6341-520": "QG-NON-AP",
            "8-6340-520": "QG-VIN-AP",
            "8-6342-520": "QG-VIN-AP",
            "8-6344-520": "QG-VIN-AP",
            "8-6346-520": "QG-VIN-AP",
            "8-6330-520": "QG-VIN-AP",
            "8-6348-520": "QG-VIN-AP",
            "8-6341-10": "QG-NON-TMO",
            "8-6343-10": "QG-NON-TMO",
            "8-6345-10": "QG-NON-TMO",
            "8-6347-10": "QG-NON-TMO",
            "8-6349-10": "QG-NON-TMO",
            "8-6340-10": "QG-VIN-TMO",
            "8-6342-10": "QG-VIN-TMO",
            "8-6344-10": "QG-VIN-TMO",
            "8-6346-10": "QG-VIN-TMO",
            "8-6348-10": "QG-VIN-TMO",
            "8-6330-10": "QG-VIN-TMO",
            "8-6350-17": "VI-VIN-Verizon",
            "8-6352-17": "VI-VIN-Verizon",
            "8-6354-17": "VI-VIN-Verizon",
            "8-6356-17": "VI-VIN-Verizon",
            "8-6332-17": "VI-VIN-Verizon",
            "8-6358-17": "VI-VIN-Verizon",
            "8-6351-17": "VI-NON-Verizon",
            "8-6333-17": "VI-NON-Verizon",
            "8-6353-17": "VI-NON-Verizon",
            "8-6355-17": "VI-NON-Verizon",
            "8-6357-17": "VI-NON-Verizon",
            "8-6359-17": "VI-NON-Verizon",
            "8-6360-10": "Arrow-67-QG",
            "8-6369-10-1001": "Arrow-67-QG",
            "8-ARLX11-M5": "Arrow-L",
            "8-ARLX11-MO": "Arrow-L",
            "8-6413-10": "Dagger-SC",
            "4-6415-510 (DO)": "Dagger-QG Large - Device Only",
        }

        df["Code"] = df["Code"].replace(code_replacements)

        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%m-%d")

        # Group by Brand, Date, and Code and sum the Qty
        df_grouped = df.groupby(["Brand", "Date", "Code"], as_index=False)["Qty"].sum()

        # Sort the dataframe by Date (ascending)
        df_sorted = df_grouped.sort_values(by="Date")

        # Rename the 'Code' column to 'Code (renamed)'
        df_sorted = df_sorted.rename(columns={"Code": "Code (renamed)"})

        # Display the resulting dataframe in Streamlit
        st.write(df_sorted, index=False)

        st.markdown(
            dataframe_to_excel_download_link(df_sorted, "MTD Results.xlsx"),
            unsafe_allow_html=True,
        )

    # Define the Streamlit app
    def main():
        # Set the title and subtitle
        st.warning("Upload a file and see the Qty count by Brand, Date, and Code.")

        if st.button("Download Template"):
            template_bytes = create_template()
            b64 = base64.b64encode(template_bytes).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="template.xlsx">Download Excel template</a>'
            st.markdown(href, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose a file (Excel or CSV)", type=["xlsx", "csv"]
        )

        # If a file was uploaded, process it
        if uploaded_file is not None:
            # Process the file and display the resulting dataframe
            process_file(uploaded_file)

    # Run the Streamlit app
    if __name__ == "__main__":
        main()

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")
