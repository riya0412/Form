import streamlit as st
import pandas as pd
from datetime import date as dt
import gspread
from google.oauth2.service_account import Credentials

# Setup Google Sheets connection
def create_connection():
    # scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # with st.secrets():
    #     # Load the JSON file
    # credentials_json = st.secrets["secrets.toml"]
    service_account_info = {
            "type": st.secrets["google_service_account"]["type"],
            "project_id": st.secrets["google_service_account"]["project_id"],
            "private_key_id": st.secrets["google_service_account"]["private_key_id"],
            "private_key": st.secrets["google_service_account"]["private_key"],
            "client_email": st.secrets["google_service_account"]["client_email"],
            "client_id": st.secrets["google_service_account"]["client_id"],
            "auth_uri": st.secrets["google_service_account"]["auth_uri"],
            "token_uri": st.secrets["google_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["google_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["google_service_account"]["client_x509_cert_url"],
            "universe_domain": "googleapis.com"
        }
        
    # Use the service account info to create credentials
    creds = Credentials.from_service_account_info(service_account_info, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)

    return client

# Function to insert godown data into the Google Sheets
def insert_godown(sheet, godown_name, from_, date, contractor):
    try:
        godown_data = [godown_name, from_, str(date), contractor]
        sheet.append_row(godown_data)
        st.session_state.godown_id = sheet.row_count
        st.success("Godown data inserted successfully")
    except Exception as e:
        st.error(f"Failed to insert data into Google Sheets: {e}")

# Function to insert bundle data into the Google Sheets
def insert_bundle(sheet, al_size, steel_size, al_percent, steel_percent, weight, is_alloy):
    try:
        is_alloy_int = 1 if is_alloy == 'YES' else 0
        bundle_data = [st.session_state.godown_id, al_size, steel_size, al_percent, steel_percent, weight, is_alloy_int]
        sheet.append_row(bundle_data)
        st.success("Bundle data inserted successfully")
    except Exception as e:
        st.error(f"Failed to insert data into Google Sheets: {e}")

# Initialize session state
if 'godown_id' not in st.session_state:
    st.session_state.godown_id = None

# Google Sheets client
client = create_connection()
spreadsheet_id1 = '1AwIlfvydwBGCOJaOjuhahG3Q3wHFh5K3xubZp2cFe_A'  # Replace with your actual spreadsheet ID
spreadsheet_id2='1HMke9Dku8Kt7tEFFuKdjRgY5RAGZhnZM2OkOhkTMCHQ'

try:
    spreadsheet1 = client.open_by_key(spreadsheet_id1)
    godown_sheet = spreadsheet1.worksheet("Godown")
    spreadsheet2 = client.open_by_key(spreadsheet_id2)
    bundle_sheet = spreadsheet2.worksheet("Unloading")
except gspread.SpreadsheetNotFound:
    st.error("Spreadsheet not found. Check the ID or permissions.")
except Exception as e:
    st.error(f"An error occurred: {e}")

# Streamlit form for Godown details
if st.session_state.godown_id is None:
    st.title("Unloading Conductors - Godown Details")

    with st.form("godown_form"):
        Godown = ["Narela", "Wazirpur", "Prahladpur", "Pooth Khurd"]
        godown_name = st.selectbox("Godown Name", options=Godown)
        Party = ["MARUTI ENTERPRISES", "SHREE SHYAM ENTERPRISES", "NAMAN INTERNATIONALv/ RYAN", "D&M CABLES",
                 "KRISHNA ENTERPRISES", "PMHSR TRANSFORMERS & CONDUCTORS PVT. LTD.", "POWER SAHAJ", "NARMADA METAL",
                 "ELECON CONDUCTORS LTD.", "JAIPURIA BROTHERS ELECTRICALS PVT. LTD.", "LAXMI WIRE INDUSTRIES",
                 "SHANTAVEER ELECTRICAL ENGG. CO.", "SRI PADMAWATI METALS", "GUPTA IMPEX", "REKHA INDUSTRIES",
                 "JM CABLE AND CONDUCTORS", "RASS HEAVY ELECTRICALS PVT LTD", "ANGOORI METALS", "LAXMI WIRE INDUSTRIES",
                 "RKS STEEL INDUSTRIES PVT LTD", "TAPODHANI METALS AND ALLOYS", "SHREE PUSHKAR WIRES",
                 "KAMYA ENTERPRISES PVT. LTD.", "MAHAVIR TRANSMISSION LIMITED", "JAIPURIA BROTHERS ELECTRICALS PVT. LTD.",
                 "SAN ELECTRICALS", "DEEPAK TRADING COMPANY", "SRI PADMAWATI METALS", "SAKAMBHARI ENTERPRISES",
                 "SHREE NATH METAL WORKS", "JAI AMBAY ELECTRICALS", "NARMADA INFRATECH AND VIDHYUT PRODUCTS PVT. LTD.",
                 "TECHNO FIBRE INDUSTRIES", "MAAN ALUMINIUM LTD.", "ARHAM INDUSTRIES", "SUMRIDHI ALUMINIUM PVT. LTD.",
                 "A.S WIRE INDUSTRIES", "SR ENTERPRISES", "PUSHPANJALI ENTERPRISES PVT LTD", "RAJ ENTERPRISES",
                 "PRAGATI ENTERPRISES", "MAHESHWARI ELECTRICALS", "GLOBAL METAL TECH", "R.L. JAIN & SONS",
                 "STAR BANGLES", "G.S TRADING COMPANY", "JAIPURIA BROTHERS", "BHALLA ENGINEERS", "RAKMAN INDUSTRIES LTD",
                 "PARMESHWAR WIRE PRODUCTS", "RISHAB POWER CONTROLS", "INDIAN QUALIY PRODUCRTS CO", "MANSA TRADING CO"]
        From_ = st.selectbox("From:", options=Party)
        date = st.date_input("Date", value=dt.today())
        Contractor = ["Contractor1", "Contractor2", "Contractor3", "Contractor4"]
        contractor = st.selectbox("Contractor who unloaded?", options=Contractor)

        submitted = st.form_submit_button("Submit")

        if submitted:
            insert_godown(godown_sheet, godown_name, From_, date, contractor)
else:
    st.title("Unloading Conductors - Bundle Details")

    with st.form("bundle_form"):
        al_size = st.number_input("Al size :")
        steel_size = st.number_input("Steel size ")
        weight = st.number_input("Weight of the bundle", min_value=0.0)
        is_alloy = st.selectbox("Is alloy?", ("YES", "NO"))

        al_percentage = 0
        steel_percentage = 0

        if al_size and steel_size:
            rad_al = al_size / 2
            rad_steel = steel_size / 2
            csa_al = 12.93 * (rad_al ** 2)
            csa_steel = 6.156 * (rad_steel ** 2)
            al_percentage = (csa_al / (csa_al + csa_steel)) * 100
            steel_percentage = (csa_steel / (csa_al + csa_steel)) * 100
        print(al_percentage)
        submitted = st.form_submit_button("Submit")

        if submitted:
            insert_bundle(bundle_sheet, al_size, steel_size, al_percentage, steel_percentage, weight, is_alloy)

    if st.button("Start New Godown Entry"):
        st.session_state.godown_id = None

# Function to fetch and display sorted data
def fetch_and_display_data():
    try:
        # Fetch all data from both sheets
        godown_data = godown_sheet.get_all_records()
        bundle_data = bundle_sheet.get_all_records()

        # Convert to dataframes
        godown_df = pd.DataFrame(godown_data)
        bundle_df = pd.DataFrame(bundle_data)

        # Merge dataframes on Godown ID
        merged_df = bundle_df.merge(godown_df, left_on='Godwon_id', right_on='Id', suffixes=('_bundle', '_godown'))

        # Sort and display
        # merged_df = merged_df.sort_values(by=['Godown', 'weight'])
        st.dataframe(merged_df)
    except Exception as e:
        st.error(f"Error fetching data from Google Sheets: {e}")

st.markdown("---")
st.header("Sorted Data")
fetch_and_display_data()
