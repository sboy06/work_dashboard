from datetime import date, datetime
from pathlib import Path
import pickle
import ssl

import gspread
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image
from urllib.request import urlopen


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
NAMES = ["", "", "", ""]
USERNAMES = ["", "", "", ""]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {"usernames": {}}

for uname, name, pwd in zip(USERNAMES, NAMES, hashed_passwords):
    user_dict = {"name": name, "password": pwd}
    credentials["usernames"].update({uname: user_dict})

authenticator = stauth.Authenticate(
    credentials, "", "", cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

try:
    if authentication_status:
        ssl._create_default_https_context = ssl._create_unverified_context

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        client = gspread.service_account(filename="service_account.json")
        database = client.open("Database")

        # gspread.sheets
        pt_ind = database.worksheet("individual")
        pt_bulk = database.worksheet("bulk")
        pt_adv = database.worksheet("advantage")
        pt_mtd = database.worksheet("MTD")

        # gspread.getrocords
        advantage = pd.DataFrame(pt_adv.get_all_records())
        bulk = pd.DataFrame(pt_bulk.get_all_records())
        individual = pd.DataFrame(pt_ind.get_all_records())

        # individual packaging
        i_date = individual["Date"]
        i_alexsamm = int(sum(individual["Alex"]))
        i_andy = int(sum(individual["Andy"]))
        i_jose_o = int(sum(individual["Jose_O"]))
        i_jesus = int(sum(individual["Jesus"]))
        i_jose_r = int(sum(individual["Jose_R"]))
        i_rolando = int(sum(individual["Rolando"]))
        i_brandon = int(sum(individual["Brandon"]))

        # bulk packaging
        b_alexsamm = int(sum(bulk["Alex"]))
        b_andy = int(sum(bulk["Andy"]))
        b_jose_o = int(sum(bulk["Jose_O"]))
        b_jesus = int(sum(bulk["Jesus"]))
        b_jose_r = int(sum(bulk["Jose_R"]))
        b_rolando = int(sum(bulk["Rolando"]))
        b_brandon = int(sum(bulk["Brandon"]))

        # advantage packaging
        mario_evo = int(sum(advantage["Mario EVO"]))
        mario_revo = int(sum(advantage["Mario REVO"]))
        andres_evo = int(sum(advantage["Andres EVO"]))
        andres_revo = int(sum(advantage["Andres REVO"]))

        # mtd total
        mtd_data = pt_mtd.get("A2:K2")
        mtd_values = [int(value) for value in mtd_data[0]]

        (
            mtd_alexsamm,
            mtd_andy,
            mtd_jose_o,
            mtd_jesus,
            mtd_jose_r,
            mtd_mario,
            mtd_rolando,
            mtd_andres,
            mtd_brandon,
        ) = mtd_values

        cds = ["Alex", "Andy", "Jose_O", "Jesus", "Jose_R", "Rolando", "Brandon"]
        adv = ["Mario EVO", "Mario REVO", "Andres EVO", "Andres REVO"]

        imageLOGO = Image.open(urlopen("https://i.ibb.co/WGjVK32/logopng.png"))
        st.image(imageLOGO)
        st.title("Packaging Team Metrics")
        st.write("---")

        # Sidebar
        st.sidebar.header(f"Welcome {name}")
        authenticator.logout("Signout", "sidebar")

        cds_team = st.sidebar.multiselect("Select CDS team member: ", cds)
        adv_team = st.sidebar.multiselect("Select Advantage team member: ", adv)

        # MTD
        mtd_ind = {
            "Alex": i_alexsamm,
            "Andy": i_andy,
            "Jose_O": i_jose_o,
            "Jesus": i_jesus,
            "Jose_R": i_jose_r,
            "Rolando": i_rolando,
            "Brandon:": i_brandon,
        }
        mtd_bulk = {
            "Alex": b_alexsamm,
            "Andy": b_andy,
            "Jose_O": b_jose_o,
            "Jesus": b_jesus,
            "Jose_R": b_jose_r,
            "Rolando": b_rolando,
            "Brandon": b_brandon,
        }
        mtd_adv = {"Mario": mtd_mario, "Andres": mtd_andres}

        mtd_mtd = {
            "Alex": mtd_alexsamm,
            "Andy": mtd_andy,
            "Jose_O": mtd_jose_o,
            "Jesus": mtd_jesus,
            "Jose_R": mtd_jose_r,
            "Mario": mtd_mario,
            "Rolando": mtd_rolando,
            "Andres": mtd_andres,
            "Brandon": mtd_brandon,
        }

        max_ind = max(mtd_ind, key=mtd_ind.get)
        max_bulk = max(mtd_bulk, key=mtd_bulk.get)
        max_adv = max(mtd_adv, key=mtd_adv.get)
        max_mtd = max(mtd_mtd, key=mtd_mtd.get)

        st.markdown(
            "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Top Packagers</h4>",
            unsafe_allow_html=True,
        )
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(
            "Top Packager", f"{str(max_mtd).replace('_', ' ')}: {(mtd_mtd[max_mtd]):,}"
        )
        col2.metric(
            "Individual Packaging",
            f"{str(max_ind).replace('_', ' ')} {(mtd_ind[max_ind]):,}",
        )
        col3.metric(
            "Bulk Packaging",
            f"{str(max_bulk.replace('_', ' '))}: {(mtd_bulk[max_bulk]):,}",
        )
        col4.metric(
            "Advantage Packaging",
            f"{str(max_adv.replace('_', ' '))}: {(mtd_adv[max_adv]):,}",
        )

        # Calculate daily averages
        daily_avg_individual = int(sum(mtd_ind.values()) / len(individual))
        daily_avg_bulk = int(sum(mtd_bulk.values()) / len(bulk))
        daily_avg_advantage = int(sum(mtd_adv.values()) / len(advantage))

        st.markdown(
            "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Daily Averages</h4>",
            unsafe_allow_html=True,
        )
        col1_avg, col2_avg, col3_avg, col4_avg = st.columns(4)
        total_average = daily_avg_individual + daily_avg_bulk + daily_avg_advantage
        col1_avg.metric("Total Average", f"{total_average:,}")
        col2_avg.metric("Individual Packaging", f"{daily_avg_individual:,}")
        col3_avg.metric("Bulk Packaging", f"{daily_avg_bulk:,}")
        col4_avg.metric("Advantage Packaging", f"{daily_avg_advantage:,}")

        # tabs
        tab1, tab2, tab3 = st.tabs(
            ["Individual Packaging", "Bulk Packaging", "Advantage Packaging"]
        )

        tab1.markdown(
            "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Line Chart</h4>",
            unsafe_allow_html=True,
        )
        tab1.subheader("")
        tab1.line_chart(individual, x="Date", y=cds_team)
        tab1.subheader("")
        tab1.write("---")
        tab1.markdown(
            "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 8px 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Top Individual Packaging 🏆</h4>",
            unsafe_allow_html=True,
        )
        packagers = {
            "Alex": i_alexsamm,
            "Andy": i_andy,
            "Jose_O": i_jose_o,
            "Jesus": i_jesus,
            "Jose_R": i_jose_r,
            "Rolando": i_rolando,
            "Brandon": i_brandon,
        }

        sorted_packagers = dict(
            sorted(packagers.items(), key=lambda x: x[1], reverse=True)
        )
        for rank, (name, value) in enumerate(sorted_packagers.items(), start=1):
            if rank == 1:
                tab1.code(f"🥇 {name.replace('_', ' ')}: {value:,}")
            elif rank == 2:
                tab1.code(f"🥈 {name.replace('_', ' ')}: {value:,}")
            elif rank == 3:
                tab1.code(f"🥉 {name.replace('_', ' ')}: {value:,}")
            elif rank <= 8:
                tab1.code(f"{rank}th {name.replace('_', ' ')}: {value:,}")
            else:
                break

        tab1.markdown("---")
        tab1.markdown(
            "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Bar Chart</h4>",
            unsafe_allow_html=True,
        )
        tab1.bar_chart(individual, x="Date", y=cds_team)
        tab1.write("---")

        tab1.table(data=individual)
        tab1.subheader("")

        tab2.markdown(
            "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Line Chart</h4>",
            unsafe_allow_html=True,
        )
        tab2.subheader("")
        tab2.line_chart(bulk, x="Date", y=cds_team)
        tab2.subheader("")
        tab2.write("---")
        tab2.markdown(
            "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 8px 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Top Bulk Packaging 🏆</h4>",
            unsafe_allow_html=True,
        )
        packagers = {
            "Alex": b_alexsamm,
            "Andy": b_andy,
            "Jose_O": b_jose_o,
            "Jesus": b_jesus,
            "Jose_R": b_jose_r,
            "Rolando": b_rolando,
            "Brandon": b_brandon,
        }

        sorted_packagers = dict(
            sorted(packagers.items(), key=lambda x: x[1], reverse=True)
        )
        for rank, (name, value) in enumerate(sorted_packagers.items(), start=1):
            if rank == 1:
                tab2.code(f"🥇 {name.replace('_', ' ')}: {value:,}")
            elif rank == 2:
                tab2.code(f"🥈 {name.replace('_', ' ')}: {value:,}")
            elif rank == 3:
                tab2.code(f"🥉 {name.replace('_', ' ')}: {value:,}")
            elif rank <= 8:
                tab2.code(f"{rank}th {name.replace('_', ' ')}: {value:,}")
            else:
                break

        tab2.markdown("---")
        tab2.markdown(
            "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Bar Chart</h4>",
            unsafe_allow_html=True,
        )
        tab2.bar_chart(bulk, x="Date", y=cds_team)
        tab2.write("---")
        tab2.table(data=bulk)
        tab2.subheader("")

        tab3.markdown(
            "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Line Chart</h4>",
            unsafe_allow_html=True,
        )
        tab3.subheader("")
        tab3.line_chart(advantage, x="Date", y=adv_team)
        tab3.subheader("")
        tab3.write("---")
        tab3.markdown(
            "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 8px 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Top Advantage Packaging 🏆</h4>",
            unsafe_allow_html=True,
        )
        packagers = {
            "Mario": mario_evo + mario_revo,
            "Andres": andres_evo + andres_revo,
        }

        sorted_packagers = dict(
            sorted(packagers.items(), key=lambda x: x[1], reverse=True)
        )
        for rank, (name, value) in enumerate(sorted_packagers.items(), start=1):
            if rank == 1:
                tab3.code(f"🥇 {name.replace('_', ' ')}: {value:,}")
            elif rank == 2:
                tab3.code(f"🥈 {name.replace('_', ' ')}: {value:,}")
            elif rank == 3:
                tab3.code(f"🥉 {name.replace('_', ' ')}: {value:,}")
            elif rank <= 8:
                tab3.code(f"{rank}th {name.replace('_', ' ')}: {value:,}")
            else:
                break

        tab3.markdown("---")
        tab3.markdown(
            "<h4 style='text-align: center; font-family: Avant Garde; align: center; padding: 5px 17px; border: 2px solid white; display: inline-block; margin: 30px 20px 40px 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);'>Bar Chart</h4>",
            unsafe_allow_html=True,
        )
        tab3.bar_chart(advantage, x="Date", y=adv_team)
        tab3.write("---")
        tab3.table(data=advantage)
        tab3.subheader("")

except (AttributeError, NameError, KeyError):
    st.warning("Please refresh the page.")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")
