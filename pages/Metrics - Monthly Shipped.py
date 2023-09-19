import pandas as pd
import gspread
import streamlit as st
import numpy as np
from PIL import Image
from urllib.request import urlopen
import pickle
import streamlit_authenticator as stauth
from pathlib import Path
from datetime import datetime
from datetime import date
from datetime import date
import ssl

current_dateTime = datetime.now()
start_dateTime = date(2022, 12, 1)

ssl._create_default_https_context = ssl._create_unverified_context

st.set_page_config(layout="wide")

# --- USER AUTHENTICATION ---
names = [
    "",
    "",
    "",
    "",
    "A",
    "E",
]
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
    credentials, " ", " ", cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    client = gspread.service_account(filename="service_account.json")
    database = client.open("Database")

    wks_brand = database.worksheet("brand")
    wks_count = database.worksheet("order_count")
    wks_pkgtype = database.worksheet("packaging_type")
    wks_device_type = database.worksheet("device_type")
    wks_harness_type = database.worksheet("harness")
    wks_revo = database.worksheet("revo")

    brand = pd.DataFrame(wks_brand.get_all_records())
    order_count = pd.DataFrame(wks_count.get_all_records())
    packaging_type = pd.DataFrame(wks_pkgtype.get_all_records())
    device_type = pd.DataFrame(wks_device_type.get_all_records())
    revo_type = pd.DataFrame(wks_revo.get_all_records())
    harness_type = pd.DataFrame(wks_harness_type.get_all_records())

    # sidebar selection options
    brands = [
        "ELO",
        "AMS",
        "Apex Protect",
        "VOXX",
        "ZAZ",
        "Safepoint",
        "Advantage",
        "Automobility",
        "Lender-Systems",
        "A1 Distributing",
        "Apex Connect",
    ]
    orders_num = ["CDS", "CDS Average", "Advantage", "ADV Average"]
    companies = ["CDS", "Advantage"]
    package_types = [
        "Elo Individual",
        "Elo Bulk",
        "Safepoint Individual",
        "Safepoint Bulk",
    ]
    device_types = ["CAN", "CAN Average", "Non-CAN", "Non-CAN Average"]
    harness_types = [
        "Domestic-VIN",
        "Domestic-Non",
        "Hardwires",
        "Universal",
        "Honda",
        "Remote-Start",
    ]
    revo_types = ["REVO1", "REVO3K", "REVOSS", "REVOSS5K"]

    # --Count from previous month--
    elo_prev_month = str(brand.iloc[-1, 1])
    ams_prev_month = str(brand.iloc[-1, 2])
    apx_prev_month = str(brand.iloc[-1, 3])
    vox_prev_month = str(brand.iloc[-1, 4])
    zaz_prev_month = str(brand.iloc[-1, 5])
    sfp_prev_month = str(brand.iloc[-1, 6])
    adv_prev_month = str(brand.iloc[-1, 7])
    atm_prev_month = str(brand.iloc[-1, 8])
    lss_prev_month = str(brand.iloc[-1, 9])
    a1d_prev_month = str(brand.iloc[-1, 10])
    apc_prev_month = str(brand.iloc[-1, 11])

    # order count
    cds_count = str(order_count.iloc[-1, 1])
    adv_count = str(order_count.iloc[-1, 3])

    # packaging type
    individual_elo = str(packaging_type.iloc[-1, 1])
    bulk_elo = str(packaging_type.iloc[-1, 2])
    individual_safepoint = str(packaging_type.iloc[-1, 3])
    bulk_safepoint = str(packaging_type.iloc[-1, 4])

    # device type
    with_can = str(device_type.iloc[-1, 1])
    non_can = str(device_type.iloc[-1, 3])

    # harness
    Domestic_VIN = str(harness_type.iloc[-1, 1])
    Domestic_NONVIN = str(harness_type.iloc[-1, 2])
    Hardwires = str(harness_type.iloc[-1, 3])
    Universal = str(harness_type.iloc[-1, 4])
    Honda = str(harness_type.iloc[-1, 5])
    Remote_Start = str(harness_type.iloc[-1, 6])

    # revo
    revo_one = str(revo_type.iloc[-1, 1])
    revo_3000 = str(revo_type.iloc[-1, 2])
    revo_smartstop = str(revo_type.iloc[-1, 3])
    revo_smartstop5K = str(revo_type.iloc[-1, 4])

    # --DF for sum / total--
    elo_total = str(sum(brand["ELO"]))
    ams_total = str(sum(brand["AMS"]))
    apx_total = str(sum(brand["Apex Protect"]))
    vox_total = str(sum(brand["VOXX"]))
    zaz_total = str(sum(brand["ZAZ"]))
    sfp_total = str(sum(brand["Safepoint"]))
    adv_total = str(sum(brand["Advantage"]))
    atm_total = str(sum(brand["Automobility"]))
    lss_total = str(sum(brand["Lender-Systems"]))
    a1d_total = str(sum(brand["A1 Distributing"]))
    apc_total = str(sum(brand["Apex Connect"]))

    # sum - packaging type
    individual_elo_total = str(sum(packaging_type["Elo Individual"]))
    bulk_elo_total = str(sum(packaging_type["Elo Bulk"]))
    individual_safepoint_total = str(sum(packaging_type["Safepoint Individual"]))
    bulk_safepoint_total = str(sum(packaging_type["Safepoint Bulk"]))

    # sum - device type
    with_can_total = str(sum(device_type["CAN"]))
    non_can_total = str(sum(device_type["Non-CAN"]))

    # sum - harness type
    DomesticVIN_total = str(sum(harness_type["Domestic-VIN"]))
    DomesticNON_total = str(sum(harness_type["Domestic-Non"]))
    Hardwires_total = str(sum(harness_type["Hardwires"]))
    Universal_total = str(sum(harness_type["Universal"]))
    Honda_total = str(sum(harness_type["Honda"]))
    RemoteStart_total = str(sum(harness_type["Remote-Start"]))

    # sum - revo type
    revo_one_total = str(sum(revo_type["REVO1"]))
    revo_3000_total = str(sum(revo_type["REVO3K"]))
    revo_SS_total = str(sum(revo_type["REVOSS"]))
    revo_SS5K_total = str(sum(revo_type["REVOSS5K"]))

    # --df for average--
    elo_avg = int(np.mean(brand["ELO"]))
    ams_avg = int(np.mean(brand["AMS"]))
    apx_avg = int(np.mean(brand["Apex Protect"]))
    vox_avg = int(np.mean(brand["VOXX"]))
    zaz_avg = int(np.mean(brand["ZAZ"]))
    sfp_avg = int(np.mean(brand["Safepoint"]))
    adv_avg = int(np.mean(brand["Advantage"]))
    atm_avg = int(np.mean(brand["Automobility"]))
    lss_avg = int(np.mean(brand["Lender-Systems"]))
    a1d_avg = int(np.mean(brand.iloc[8:, 10]))
    apc_avg = int(np.mean(brand.iloc[9:, 11]))

    # average - order count
    cds_avg = int(np.mean(order_count["CDS"]))
    adv_order_avg = int(np.mean(order_count["Advantage"]))

    # average - packaging type
    individual_elo_average = int(np.mean(packaging_type["Elo Individual"]))
    bulk_elo_average = int(np.mean(packaging_type["Elo Bulk"]))
    individual_safepoint_average = int(np.mean(packaging_type["Safepoint Individual"]))
    bulk_safepoint_average = int(np.mean(packaging_type["Safepoint Bulk"]))

    # average - device type
    with_can_average = int(np.mean(device_type["CAN"]))
    non_can_average = int(np.mean(device_type["Non-CAN"]))

    # average - harness type
    DomesticVIN_average = int(np.mean(harness_type["Domestic-VIN"]))
    DomesticNON_average = int(np.mean(harness_type["Domestic-Non"]))
    Hardwires_average = int(np.mean(harness_type["Hardwires"]))
    Universal_average = int(np.mean(harness_type["Universal"]))
    Honda_average = int(np.mean(harness_type["Honda"]))
    RemoteStart_average = int(np.mean(harness_type["Remote-Start"]))

    # average - revo type
    revo_one_average = int(np.mean(revo_type["REVO1"]))
    revo_3000_average = int(np.mean(revo_type["REVO3K"]))
    revo_SS_average = int(np.mean(revo_type["REVOSS"]))
    revo_SS5K_average = int(np.mean(revo_type["REVOSS5K"]))

    # --calculate percentage--

    # order counts % out of 100
    CDS_orders = int(cds_count)
    ADV_orders = int(adv_count)
    total_orders = CDS_orders + ADV_orders

    CDS = (CDS_orders / total_orders) * 100
    ADV = (ADV_orders / total_orders) * 100
    round_CDS = round(CDS)
    round_ADV = round(ADV)

    # device type % out of 100
    CAN_device = int(with_can)
    NonCAN_device = int(non_can)
    total_devices = CAN_device + NonCAN_device

    CAN = (CAN_device / total_devices) * 100
    NONCAN = (NonCAN_device / total_devices) * 100
    round_CAN = round(CAN)
    round_NONCAN = round(NONCAN)

    # revo type % out of 100
    revo_one_number = int(revo_one)
    revo_3000_number = int(revo_3000)
    revo_smartstop_number = int(revo_smartstop)
    revo_smartstop5K_number = int(revo_smartstop5K)
    total_revo = (
        revo_one_number
        + revo_3000_number
        + revo_smartstop_number
        + revo_smartstop5K_number
    )

    REVO_ONE = (revo_one_number / total_revo) * 100
    REVO_3000 = (revo_3000_number / total_revo) * 100
    REVO_SS = (revo_smartstop_number / total_revo) * 100
    REVO_SS5K = (revo_smartstop5K_number / total_revo) * 100
    round_ONE = round(REVO_ONE)
    round_3000 = round(REVO_3000)
    round_SS = round(REVO_SS)
    round_SS5K = round(REVO_SS5K)

    imageLOGO = Image.open(urlopen("https://i.ibb.co/WGjVK32/logopng.png"))
    st.image(imageLOGO)
    st.title("Monthly Shipped")
    st.set_option("deprecation.showPyplotGlobalUse", False)

    # Hide 'Made with Streamlit' & app menu
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.header(f"Welcome {name}")
    authenticator.logout("Signout", "sidebar")
    st.sidebar.subheader("Shipped Metrics Selection")

    brand_selection = st.sidebar.multiselect("Select brand: ", brands)
    ordernum_selection = st.sidebar.multiselect("Select order counts:", companies)
    packagingtype_selection = st.sidebar.multiselect(
        "Select packaging type:", package_types
    )
    device_type_selection = st.sidebar.multiselect("Select device type:", device_types)
    harness_type_selection = st.sidebar.multiselect("Select harness:", harness_types)
    revo_types_selection = st.sidebar.multiselect(
        "Select REVO service type:", revo_types
    )

    # tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Brands",
            "Order Counts",
            "CDS Packaging Types",
            "Device Types",
            "Harness Types",
            "REVO Type",
        ]
    )
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("ELO", elo_prev_month)
        col2.metric("ELO Average", str(elo_avg))
        col3.metric("Advantage", adv_prev_month)
        col4.metric("Advantage Average", str(adv_avg))

    with tab1:
        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Apex Protect", apx_prev_month)
        col6.metric("Apex Average", str(apx_avg))
        col7.metric("VOXX Intl", vox_prev_month)
        col8.metric("VOXX Average", str(vox_avg))

    with tab1:
        col9, col10, col11, col12 = st.columns(4)
        col9.metric("ZAZ GPS", zaz_prev_month)
        col10.metric("ZAZ Average", str(zaz_avg))
        col11.metric("Safepoint GPS", sfp_prev_month)
        col12.metric("Safepoint Average", str(sfp_avg))

    with tab1:
        col13, col14, col15, col16 = st.columns(4)
        col13.metric("AMS", ams_prev_month)
        col14.metric("AMS Average", str(ams_avg))
        col15.metric("Automobility", atm_prev_month)
        col16.metric("Automobility Average", str(atm_avg))

    with tab1:
        col17, col18, col19, col20 = st.columns(4)
        col17.metric("Lender Systems", lss_prev_month)
        col18.metric("Lender Systems Average", str(lss_avg))
        col19.metric("A1 Distributing", a1d_prev_month)
        col20.metric("A1D Average", str(a1d_avg))

    with tab1:
        col21, col22, col23, col24 = st.columns(4)
        col21.metric("Apex Connect", apc_prev_month)
        col22.metric("Apex Connect Average", str(apc_avg))

    tab1.subheader("Chart")
    tab1.subheader("")
    tab1.line_chart(brand, x="End of Month", y=brand_selection, width=300, height=500)
    tab1.subheader("Data")
    tab1.table(data=brand.tail(12))
    tab1.subheader("")
    tab1.subheader("Total")
    tab1.code(f"ELO: {elo_total}")
    tab1.code(f"AMS: {ams_total}")
    tab1.code(f"Apex Protect: {apx_total}")
    tab1.code(f"VOXX: {vox_total}")
    tab1.code(f"ZAZ GPS: {zaz_total}")
    tab1.code(f"Safepoint GPS: {sfp_total}")
    tab1.code(f"Advantage GPS: {adv_total}")
    tab1.code(f"Automobility: {atm_total}")
    tab1.code(f"Lender-Systems: {lss_total}")
    tab1.code(f"A1 Distributing: {a1d_total}")
    tab1.code(f"Apex Connect: {apc_total}")

    with tab2:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CDS Order Count", cds_count)
        col2.metric("CDS Average", str(cds_avg))
        col3.metric("Advantage", adv_count)
        col4.metric("Advantage Average", str(adv_order_avg))

    with tab2:
        st.subheader("Percentage")
        col5, col6 = st.columns(2)
        col5.metric("Connected Dealer Services", "%s%%" % round_CDS)
        col6.metric("Advantage GPS", "%s%%" % round_ADV)

    tab2.subheader("Chart")
    tab2.subheader("")
    tab2.line_chart(
        order_count, x="End of Month", y=ordernum_selection, width=300, height=500
    )
    tab2.subheader("Data")
    tab2.table(data=order_count.tail(12))
    tab2.subheader("")
    tab2.subheader("Total")
    tab2.code(f"CDS: {cds_count}")
    tab2.code(f"Advantage: {adv_count}")

    with tab3:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("ELO Individual", individual_elo)
        col2.metric("ELO Individual Average", str(individual_elo_average))
        col3.metric("ELO Bulk", bulk_elo)
        col4.metric("ELO Bulk Average", str(bulk_elo_average))

    with tab3:
        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Safepoint Individual", individual_safepoint)
        col6.metric("Safepoint Individual Average", str(individual_safepoint_average))
        col7.metric("Safepoint Bulk", bulk_safepoint)
        col8.metric("Safepoint Bulk Average", str(bulk_safepoint_average))

    tab3.subheader("Chart")
    tab3.subheader("")
    tab3.line_chart(
        packaging_type,
        x="End of Month",
        y=packagingtype_selection,
        width=300,
        height=500,
    )
    tab3.subheader("Data")
    tab3.table(data=packaging_type.tail(12))
    tab3.subheader("")
    tab3.subheader("Total")
    tab3.code(f"ELO Individual: {individual_elo_total}")
    tab3.code(f"ELO Bulk: {bulk_elo_total}")
    tab3.code(f"Safepoint Individual: {individual_safepoint_total}")
    tab3.code(f"Safepoint Bulk: {bulk_safepoint_total}")

    with tab4:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CAN", with_can)
        col2.metric("CAN Average", str(with_can_average))
        col3.metric("Non-CAN", non_can)
        col4.metric("Non-CAN Average", str(non_can_average))

    with tab4:
        st.subheader("Percentage")
        col5, col6 = st.columns(2)
        col5.metric("CAN", "%s%%" % round_CAN)
        col6.metric("Non-CAN", "%s%%" % round_NONCAN)

    tab4.subheader("Chart")
    tab4.subheader("")
    tab4.line_chart(
        device_type, x="End of Month", y=device_type_selection, width=300, height=500
    )
    tab4.subheader("Data")
    tab4.table(data=device_type.tail(12))
    tab4.subheader("")
    tab4.subheader("Total")
    tab4.code(f"CAN device: {with_can_total}")
    tab4.code(f"Non-CAN device: {non_can_total}")

    with tab5:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Domestic VIN", Domestic_VIN)
        col2.metric("Domestic VIN Average", str(DomesticVIN_average))
        col3.metric("Domestic Non-VIN", Domestic_NONVIN)
        col4.metric("Domestic Non-VIN Average", str(DomesticNON_average))

    with tab5:
        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Hardwires", Hardwires)
        col6.metric("Hardwires Average", str(Hardwires_average))
        col7.metric("Universal OBDII Harness", Universal)
        col8.metric("Universal OBDII Average", str(Universal_average))

    with tab5:
        col9, col10, col11, col12 = st.columns(4)
        col9.metric("Honda", Honda)
        col10.metric("Honda Average", str(Honda_average))
        col11.metric("Remote Start Kits", Remote_Start)
        col12.metric("Remote Start Average", str(RemoteStart_average))

    tab5.subheader("Chart")
    tab5.subheader("")
    tab5.line_chart(
        harness_type, x="End of Month", y=harness_type_selection, width=300, height=500
    )
    tab5.subheader("Data")
    tab5.table(data=harness_type.tail(12))
    tab5.subheader("")
    tab5.subheader("Total")
    tab5.code(f"Domestic VIN: {DomesticVIN_total}")
    tab5.code(f"Domestic NON-VIN: {DomesticNON_total}")
    tab5.code(f"Hardwires: {Hardwires_total}")
    tab5.code(f"Universal OBDII Kit: {Universal_total}")
    tab5.code(f"Honda: {Honda_total}")
    tab5.code(f"Remote Start: {RemoteStart_total}")

    with tab6:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("REVO ONE", revo_one)
        col2.metric("REVO ONE Average", str(revo_one_average))
        col3.metric("REVO 3000", revo_3000)
        col4.metric("REVO 3000 Average", str(revo_3000_average))

    with tab6:
        col5, col6, col7, col8 = st.columns(4)
        col5.metric("REVO SS", revo_smartstop)
        col6.metric("REVO SmartStop Average", str(revo_SS_average))
        col7.metric("REVO SS5K", revo_smartstop5K)
        col8.metric("REVO SmartStop-5K Average", str(revo_SS5K_average))

    with tab6:
        st.write("-- Percentage --")
        col9, col10, col11, col12 = st.columns(4)
        col9.metric("REVO ONE", "%s%%" % round_ONE)
        col10.metric("REVO 3000", "%s%%" % round_3000)
        col11.metric("REVO SmartStop", "%s%%" % round_SS)
        col12.metric("REVO SmartStop-5K", "%s%%" % round_SS5K)

    tab6.subheader("Chart")
    tab6.subheader("")
    tab6.line_chart(
        revo_type, x="End of Month", y=revo_types_selection, width=300, height=500
    )
    tab6.subheader("Data")
    tab6.table(data=revo_type.tail(12))
    tab6.subheader("")
    tab6.subheader("Total")
    tab6.code(f"REVO ONE: {revo_one_total}")
    tab6.code(f"REVO 3K: {revo_3000_total}")
    tab6.code(f"REVO SmartStop: {revo_SS_total}")
    tab6.code(f"REVO SmartStop-5K: {revo_SS5K_total}")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")
