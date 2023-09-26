import pandas as pd
import numpy as np
import gspread
import streamlit as st
import ssl
from PIL import Image
from urllib.request import urlopen
import pickle
import streamlit_authenticator as stauth
from pathlib import Path
from datetime import datetime
from datetime import date
import datetime as dt
import datetime
import plotly.express as px
from streamlit_extras.app_logo import add_logo

ssl._create_default_https_context = ssl._create_unverified_context
st.set_page_config(layout="wide")
add_logo("https://i.ibb.co/WGjVK32/logopng.png")

try:

    class QA_Tracker:
        def __init__(self):
            self.st = st
            self.start_dateTime = date(2022, 12, 1)
            self.today = datetime.datetime.now()
            self.current_month = self.today.month
            self.current_year = self.today.year

            self.hide_streamlit_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
            self.st.markdown(self.hide_streamlit_style, unsafe_allow_html=True)
            self.force_dark_mode_style = """
            <style>
            /* Override background color */
            body {
                background-color: #0e1117 !important;
            }
            /* Override text color, etc */
            </style>
            """

            st.markdown(self.force_dark_mode_style, unsafe_allow_html=True)

            self.names = [
                "",
                "",
                "",
                "",
                "",
                "",
            ]
            self.usernames = [
                "",
                "",
                "",
                "",
                "",
                "",
            ]
            self.file_path = Path(__file__).parent / "hashed_pw.pkl"
            self.credentials = {"usernames": {}}
            self.authenticator = stauth.Authenticate(
                self.credentials, "<any>", "<random>", cookie_expiry_days=60
            )

        def load_data(self):
            with self.file_path.open("rb") as file:
                self.hashed_passwords = pickle.load(file)
            for uname, name, pwd in zip(
                self.usernames, self.names, self.hashed_passwords
            ):
                user_dict = {"name": name, "password": pwd}
                self.credentials["usernames"].update({uname: user_dict})

        def authenticate(self):
            (
                self.name,
                self.authentication_status,
                self.username,
            ) = self.authenticator.login("Login", "main")

        def access_spreadsheet(self):
            if self.authentication_status:
                self.scope = [
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive",
                ]
                client = gspread.service_account(filename="service_account.json")
                self.database = client.open("Database")

                self.device_management_arrow = self.database.worksheet("arrow_qa")
                self.device_management_dagger = self.database.worksheet("dagger_qa")
                self.device_management_adrian_c = self.database.worksheet("Adrian_C")
                self.device_management_adrian_h = self.database.worksheet("Adrian_H")
                self.device_management_jesse = self.database.worksheet("Jesse")
                self.device_management_eddie_b = self.database.worksheet("Eddie_B")

                self.arrow_qa = pd.DataFrame(
                    self.device_management_arrow.get_all_records()
                )
                self.dagger_qa = pd.DataFrame(
                    self.device_management_dagger.get_all_records()
                )
                self.adrian_c_qa = pd.DataFrame(
                    self.device_management_adrian_c.get_all_records()
                )
                self.adrian_h_qa = pd.DataFrame(
                    self.device_management_adrian_h.get_all_records()
                )
                self.jesse_qa = pd.DataFrame(
                    self.device_management_jesse.get_all_records()
                )
                self.eddie_b_qa = pd.DataFrame(
                    self.device_management_eddie_b.get_all_records()
                )

        def process_data(self):
            self.arrow_passed_qty = self.arrow_qa["Quantity"]
            self.dagger_passed_qty = self.dagger_qa["Quantity"]

            self.arrow_qa["Date"] = pd.to_datetime(self.arrow_qa["Date"])
            self.dagger_qa["Date"] = pd.to_datetime(self.dagger_qa["Date"])

            self.arrow_qa = self.arrow_qa.sort_values(by="Date")
            self.dagger_qa = self.dagger_qa.sort_values(by="Date")

            self.dates_passed_arrow = self.arrow_qa["Date"]
            self.dates_passed_dagger = self.dagger_qa["Date"]

            self.arrow_passed_average = int(np.mean(self.arrow_qa["Quantity"]))
            self.dagger_passed_average = int(np.mean(self.dagger_qa["Quantity"]))
            self.adrian_calletano_average = int(np.mean(self.adrian_c_qa["Quantity"]))
            self.adrian_hernandez_average = int(np.mean(self.adrian_h_qa["Quantity"]))
            self.jesse_ortiz_average = int(np.mean(self.jesse_qa["Quantity"]))
            self.eddie_blanco_average = int(np.mean(self.eddie_b_qa["Quantity"]))

            self.monthtodate_arrow = self.arrow_qa[
                (self.dates_passed_arrow.dt.month == self.current_month)
                & (self.dates_passed_arrow.dt.year == self.current_year)
            ]
            self.monthtodate_dagger = self.dagger_qa[
                (self.dates_passed_dagger.dt.month == self.current_month)
                & (self.dates_passed_dagger.dt.year == self.current_year)
            ]

            self.monthtodate_arrow["Date"] = self.monthtodate_arrow["Date"].dt.strftime(
                "%Y-%m-%d"
            )
            self.monthtodate_dagger["Date"] = self.monthtodate_dagger[
                "Date"
            ].dt.strftime("%Y-%m-%d")

            self.mtd_arrow = self.monthtodate_arrow["Quantity"]
            self.mtd_dagger = self.monthtodate_dagger["Quantity"]

            self.ytd_arrow = self.arrow_qa[
                self.dates_passed_arrow.dt.year == self.current_year
            ]
            self.ytd_dagger = self.dagger_qa[
                self.dates_passed_dagger.dt.year == self.current_year
            ]

            self.ytd_arrow_qty = self.ytd_arrow["Quantity"]
            self.ytd_dagger_qty = self.ytd_dagger["Quantity"]

            self.ytd_arrow_average = int(np.mean(self.ytd_arrow_qty))
            self.ytd_dagger_average = int(np.mean(self.ytd_dagger_qty))

            try:
                self._extracted_from_process_data_50()
            except Exception as e:
                print(f"An error occurred: {e}")

        def _extracted_from_process_data_50(self):
            self.adrian_c_qa["Date"] = pd.to_datetime(self.adrian_c_qa["Date"])
            self.adrian_h_qa["Date"] = pd.to_datetime(self.adrian_h_qa["Date"])
            self.jesse_qa["Date"] = pd.to_datetime(self.jesse_qa["Date"])
            self.eddie_b_qa["Date"] = pd.to_datetime(self.eddie_b_qa["Date"])

            self.adrian_c_mtd = (
                self.adrian_c_qa[
                    self.adrian_c_qa["Date"].dt.month == self.current_month
                ]["Quantity"]
                .astype(int)
                .sum()
            )
            self.adrian_h_mtd = (
                self.adrian_h_qa[
                    self.adrian_h_qa["Date"].dt.month == self.current_month
                ]["Quantity"]
                .astype(int)
                .sum()
            )
            self.jesse_mtd = (
                self.jesse_qa[self.jesse_qa["Date"].dt.month == self.current_month][
                    "Quantity"
                ]
                .astype(int)
                .sum()
            )
            self.eddie_b_mtd = (
                self.eddie_b_qa[self.eddie_b_qa["Date"].dt.month == self.current_month][
                    "Quantity"
                ]
                .astype(int)
                .sum()
            )


        def display_data(self):
            st.markdown(
                    "<h1 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; display: inline-block; margin: 30px 20px 10px -50px;'>Device Management: QA Tracker</h1>",
                    unsafe_allow_html=True,
                )

            st.markdown("---")
            st.write("")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric(
                "Arrow: Daily QA'd Average",
                "{:,}".format(self.arrow_passed_average),
            )
            col2.metric(
                "Dagger: Daily QA'd Average",
                "{:,}".format(self.dagger_passed_average),
            )
            col3.metric(
                "Arrow: YTD Daily Average QA'd Devices",
                "{:,}".format(self.ytd_arrow_average),
            )
            col4.metric(
                "Dagger: YTD Daily Average QA'd Devices",
                "{:,}".format(self.ytd_dagger_average),
            )

            col5, col6, col7, col8 = st.columns(4)
            col5.metric(
                "Arrow: MTD QA'd Devices",
                "{:,}".format(self.mtd_arrow.sum()), 
            )
            col6.metric(
                "Dagger: MTD QA'd Devices",
                "{:,}".format(self.mtd_dagger.sum()),
            )
            col7.metric(
                "Arrow: YTD Total QA'd Devices",
                "{:,}".format(self.ytd_arrow_qty.sum()),
            )
            col8.metric(
                "Dagger: YTD Total QA'd Devices",
                "{:,}".format(self.ytd_dagger_qty.sum()),

            )

            tab1, tab2, tab3 = st.tabs(["Arrow", "Dagger", "Team Metrics"])

            with tab1:
                st.markdown(
                    "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 0px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Arrow</h4>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<h6 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; display: inline-block; margin: 30px 20px 40px 0px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Line ChartChart</h6>",
                    unsafe_allow_html=True,
                )
                st.line_chart(
                    self.arrow_qa, x="Date", y="Quantity", width=150, height=300
                )
                st.markdown(
                    "<h6 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; display: inline-block; margin: 30px 20px 40px 0px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Month-to-Date Bar Chart</h6>",
                    unsafe_allow_html=True,
                )
                st.bar_chart(
                    self.monthtodate_arrow,
                    x="Date",
                    y="Quantity",
                    width=150,
                    height=300,
                )

            with tab2:
                st.markdown(
                    "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 0px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Dagger</h4>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<h6 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; display: inline-block; margin: 30px 20px 40px 0px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Line ChartChart</h6>",
                    unsafe_allow_html=True,
                )
                st.line_chart(
                    self.dagger_qa, x="Date", y="Quantity", width=150, height=300
                )
                st.markdown(
                    "<h6 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; display: inline-block; margin: 30px 20px 40px 0px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Month-to-Date Bar Chart</h6>",
                    unsafe_allow_html=True,
                )
                st.bar_chart(
                    self.monthtodate_dagger,
                    x="Date",
                    y="Quantity",
                    width=150,
                    height=300,
                )

            with tab3:
                st.markdown(
                    "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 0px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Top Team Members</h4>",
                    unsafe_allow_html=True,
                )

                packagers = {
                    "Adrian_Calletano": self.adrian_c_mtd,
                    "Adrian_Hernandez": self.adrian_h_mtd,
                    "Jesse_Ortiz": self.jesse_mtd,
                    "Eddie_Blanco": self.eddie_b_mtd,
                }

                sorted_packagers = dict(
                    sorted(packagers.items(), key=lambda x: x[1], reverse=True)
                )
                for rank, (name, value) in enumerate(sorted_packagers.items(), start=1):
                    if rank == 1:
                        tab3.code(
                            f"🥇 {name.replace('_', ' ')}: {value:,}"
                        )
                    elif rank == 2:
                        tab3.code(
                            f"🥈 {name.replace('_', ' ')}: {value:,}"
                        )
                    elif rank == 3:
                        tab3.code(
                            f"🥉 {name.replace('_', ' ')}: {value:,}"
                        )
                    elif rank <= 8:
                        tab3.code(
                            f"{rank}th {name.replace('_', ' ')}: {value:,}"
                        )
                    else:
                        break

                st.markdown("---")
                st.markdown(
                    "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 30px 0px; ; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Pie Chart</h4>",
                    unsafe_allow_html=True,
                )
                labels = ['Adrian Calletano', 'Adrian Hernandez', 'Jesse Ortiz', 'Eddie Blanco']
                values = [self.adrian_c_mtd, self.adrian_h_mtd, self.jesse_mtd, self.eddie_b_mtd]
                
                fig = px.pie(
                    values=values, 
                    names=labels,
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    title='MTD Team % Comparison',
                    hole=.3
                )
                fig.update_layout(width=900, height=700)
                fig.update_traces(textinfo='percent+label', pull=[0.04, 0.04, 0.04, 0.04])
                st.plotly_chart(fig, use_container_width=False)

                st.markdown("---")
                st.markdown(
                    "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 30px 0px; ; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>MTD: Individual Daily Averages</h4>",
                    unsafe_allow_html=True,
                )
                st.markdown("")

                col9, col10, col11, col12 = st.columns(4)

                col9.metric(
                    "Adrian Calletano", "{:,}".format(self.adrian_calletano_average)
                )
                col10.metric(
                    "Adrian Hernandez", "{:,}".format(self.adrian_hernandez_average)
                )
                col11.metric("Jesse Ortiz", "{:,}".format(self.jesse_ortiz_average))
                col12.metric("Eddie Blanco", "{:,}".format(self.eddie_blanco_average))

                st.markdown("---")
                st.write("")
                st.markdown("<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 30px 0px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'> Bubble Chart of Daily Averages</h4>",
                            unsafe_allow_html=True)
                bubble_data = {
                    'Team Members': ['Adrian Calletano', 'Adrian Hernandez', 'Jesse Ortiz', 'Eddie Blanco'],
                    'Individual Averages': [self.adrian_calletano_average, self.adrian_hernandez_average, self.jesse_ortiz_average, self.eddie_blanco_average],
                }
                df_bubble = pd.DataFrame(bubble_data)

                fig = px.scatter(df_bubble, x='Team Members', y='Individual Averages', size='Individual Averages', color='Team Members')
                st.plotly_chart(fig)

                st.markdown("---")
                st.write("")

                col13, col14, col15, col16 = st.columns(4)

                col13.markdown(
                    "<h6 style='text-align: center; font-family: Avant Garde; align: center; padding: 10px 17px; border: 2px solid white; display: inline-block; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2); margin: 8px 0px'>Adrian Calletano</h6>",
                    unsafe_allow_html=True,
                )
                col13.dataframe(self.adrian_c_qa, hide_index=True)
                col13.markdown("")

                col14.markdown(
                    "<h6 style='text-align: center; font-family: Avant Garde; align: center; padding: 10px 14px; border: 2px solid white; display: inline-block; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2); margin: 8px 0px'>Adrian Hernandez</h6>",
                    unsafe_allow_html=True,
                )
                col14.dataframe(self.adrian_h_qa, hide_index=True)
                col14.markdown("")

                col15.markdown(
                    "<h6 style='text-align: center; font-family: Avant Garde; align: center; padding: 10px 39px; border: 2px solid white; display: inline-block; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2); margin: 8px 0px'>Jesse Ortiz</h6>",
                    unsafe_allow_html=True,
                )
                col15.dataframe(self.jesse_qa, hide_index=True)
                col15.markdown("")

                col16.markdown(
                    "<h6 style='text-align: center; font-family: Avant Garde; align: center; padding: 10px 30px; border: 2px solid white; display: inline-block; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2); margin: 8px 0px'>Eddie Blanco</h6>",
                    unsafe_allow_html=True,
                )
                col16.dataframe(self.eddie_b_qa, hide_index=True)
                col16.markdown("")

    if __name__ == "__main__":
        tracker = QA_Tracker()
        tracker.load_data()
        tracker.authenticate()
        tracker.access_spreadsheet()
        tracker.process_data()
        tracker.display_data()

except (AttributeError, NameError, KeyError):
    print("Please refresh the page.")
