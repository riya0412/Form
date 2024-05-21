import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import date as dt

def app():
    # Database connection function
    def create_connection():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='Kuber_Inventory',
                user='root',
                password='Pars@0412'
            )
            if connection.is_connected():
                return connection
        except Error as e:
            st.error(f"Error while connecting to MySQL: {e}")
            return None

    # Function to insert godown data into the database
    def insert_godown(godown_name,from_, date, contractor):
        connection = create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                query = """INSERT INTO Godown (Godown,From_, Date_of_unloading, Contactor) 
                        VALUES (%s, %s, %s,%s)"""
                cursor.execute(query, (godown_name,from_, date, contractor))
                connection.commit()
                st.session_state.godown_id = cursor.lastrowid
                st.success("Godown data inserted successfully")
            except Error as e:
                st.error(f"Failed to insert data into MySQL table: {e}")
            finally:
                cursor.close()
                connection.close()

    # Function to insert bundle data into the database
    def insert_bundle(al_size, steel_size,al_percent,steel_percent, weight, is_alloy):
        connection = create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                is_alloy_int = 1 if is_alloy == 'Y' else 0
                query = """INSERT INTO Unloading (Godwon_id, al_size, steel_size,al_percentage,steel_percentage, weight, alloy) 
                        VALUES (%s, %s, %s, %s, %s,%s,%s)"""
                cursor.execute(query, (st.session_state.godown_id, al_size, steel_size,al_percent,steel_percent, weight, is_alloy_int))
                connection.commit()
                st.success("Bundle data inserted successfully")
            except Error as e:
                st.error(f"Failed to insert data into MySQL table: {e}")
            finally:
                cursor.close()
                connection.close()

    # Initialize session state
    if 'godown_id' not in st.session_state:
        st.session_state.godown_id = None

    # Streamlit form for Godown details
    if st.session_state.godown_id is None:
        st.title("Unloading Conductors - Godown Details")

        with st.form("godown_form"):
            Godown=["Narela","Wazirpur","Prahladpur","Pooth Khurd"]
            godown_name = st.selectbox("Godown Name",options=Godown)
            From_ = st.text_input("From:")
            date = st.date_input("Date", value=dt.today())
            contractor = st.text_input("Contractor who unloaded?")

            submitted = st.form_submit_button("Submit")

            if submitted:
                insert_godown(godown_name,From_, date, contractor)
    else:
        st.title("Unloading Conductors - Bundle Details")

        with st.form("bundle_form"):
            al_size = st.number_input("Al size :")
            steel_size = st.number_input("Steel size ")
            weight = st.number_input("Weight of the bundle", min_value=0.0)
            is_alloy = st.selectbox("Is alloy?", ("Y", "N"))

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
                insert_bundle(al_size, steel_size,al_percentage, steel_percentage, weight, is_alloy)

        if st.button("Start New Godown Entry"):
            st.session_state.godown_id = None

    # Function to fetch and display sorted data
    def fetch_and_display_data():
        connection = create_connection()
        if connection is not None:
            cursor = connection.cursor(dictionary=True)
            try:
                # Query to fetch bundle data and count bundles per godown
                query = """
                    SELECT b.al_size, b.steel_size,b.al_percentage,b.steel_percentage, b.weight, b.alloy, g.Godown,g.From_, g.Date_of_unloading, g.Contactor,
                        COUNT(b.id) OVER (PARTITION BY b.Godwon_id) AS total_bundles,
                        ROW_NUMBER() OVER (PARTITION BY b.Godwon_id ORDER BY b.id) AS bundle_number
                    FROM Unloading b
                    JOIN Godown g ON b.Godwon_id = g.Id
                    ORDER BY g.Godown, b.weight
                """
                cursor.execute(query)
                records = cursor.fetchall()

                for record in records:
                    weight = record["weight"]
                    color = "red" if weight < 50 else "black"
                    is_alloy_str = 'Y' if record["alloy"] == 1 else 'N'
                    st.markdown(
                        f"<span style='color: {color};'>{record['al_size']} | {record['steel_size']} | {record['al_percentage']} | {record['steel_percentage']} | "
                        f"{record['weight']} | {is_alloy_str} | {record['Godown']} | "
                        f"{record['Date_of_unloading']} | {record['Contactor']} | "
                        f"Bundle {record['bundle_number']} of {record['total_bundles']}</span>",
                        unsafe_allow_html=True,
                    )
            except Error as e:
                st.error(f"Error fetching data from MySQL table: {e}")
            finally:
                cursor.close()
                connection.close()

    st.markdown("---")
    st.header("Sorted Data")
    fetch_and_display_data()
