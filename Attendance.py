import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def app():
    # Lunch break duration in hours
    lunch_break_duration = 1  # 1 hour

    # Function to calculate working hours excluding lunch break
    def calculate_working_hours(in_time, out_time):
        total_hours = (out_time - in_time).seconds / 3600
        working_hours = total_hours - lunch_break_duration
        return working_hours if working_hours > 0 else 0

    # Function to load Excel data
    def load_data(file):
        data = pd.read_excel(file, engine='openpyxl')
        return data

    # Title of the app
    st.title("Employee Attendance System")

    # Sidebar for manual entry
    st.sidebar.header("Manual Entry")
    employee_id = st.sidebar.text_input("Employee ID")
    employee_name = st.sidebar.text_input("Employee Name")
    position = st.sidebar.text_input("Position")
    in_time = st.sidebar.time_input("In Time")
    out_time = st.sidebar.time_input("Out Time")
    submit = st.sidebar.button("Submit Attendance")

    # File uploader for Excel file
    uploaded_file = st.file_uploader("Biometric Attendance Sheet Excel", type=["xlsx"])

    if uploaded_file:
        df = load_data(uploaded_file)
        st.write("Excel Data", df)

        # Process Excel data
        df['Date'] = pd.to_datetime(df['Date'])
        # df['Time'] = pd.to_datetime(df['Time']).dt.time
        df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))

        # Filter IN and OUT records
        df_in = df[df['IN_or_OUT'] == 'IN'].copy()
        df_out = df[df['IN_or_OUT'] == 'OUT'].copy()

        # Merge IN and OUT records
        df_merged = pd.merge(df_in, df_out, on=['EmployeeID', 'EmployeeName', 'Position', 'Date'], suffixes=('_in', '_out'))
        df_merged['In Time'] = pd.to_datetime(df_merged['Date'].astype(str) + ' ' + df_merged['Time_in'].astype(str))
        df_merged['Out Time'] = pd.to_datetime(df_merged['Date'].astype(str) + ' ' + df_merged['Time_out'].astype(str))
        df_merged['Working Hours'] = df_merged.apply(lambda row: calculate_working_hours(row['In Time'], row['Out Time']), axis=1)
        st.write("Processed Data", df_merged)

        # Summary of total working hours for each employee per month
        df_merged['Month'] = df_merged['In Time'].dt.to_period('M')
        summary = df_merged.groupby(['EmployeeID', 'EmployeeName', 'Position', 'Month']).agg({'Working Hours': 'sum'}).reset_index()
        pivot_summary = summary.pivot_table(index=['EmployeeID', 'EmployeeName', 'Position'], columns='Month', values='Working Hours', fill_value=0).reset_index()
        st.write("Monthly Summary", pivot_summary)

    # Handling manual entry
    if submit:
        if employee_id and employee_name and position and in_time and out_time:
            in_time_dt = datetime.combine(datetime.today(), in_time)
            out_time_dt = datetime.combine(datetime.today(), out_time)
            working_hours = calculate_working_hours(in_time_dt, out_time_dt)
            
            manual_data = {
                "EmployeeID": [employee_id],
                "EmployeeName": [employee_name],
                "Position": [position],
                "In Time": [in_time_dt],
                "Out Time": [out_time_dt],
                "Working Hours": [working_hours],
                "Month": [in_time_dt.strftime('%Y-%m')]
            }
            
            manual_df = pd.DataFrame(manual_data)
            st.write("Manual Entry Data", manual_df)
            
            # Save manual entry to a global DataFrame (optional step)
            if 'manual_entries' not in st.session_state:
                st.session_state.manual_entries = pd.DataFrame(columns=manual_df.columns)
            
            st.session_state.manual_entries = pd.concat([st.session_state.manual_entries, manual_df], ignore_index=True)
            st.write("All Manual Entries", st.session_state.manual_entries)
            
            st.success("Attendance recorded successfully!")
        else:
            st.error("Please fill out all fields")

    # Combining manual and Excel entries for final summary
    if uploaded_file or submit:
        if 'manual_entries' in st.session_state:
            combined_df = pd.concat([df_merged[['EmployeeID', 'EmployeeName', 'Position', 'Month', 'Working Hours']], st.session_state.manual_entries[['EmployeeID', 'EmployeeName', 'Position', 'Month', 'Working Hours']]], ignore_index=True)
        else:
            combined_df = df_merged[['EmployeeID', 'EmployeeName', 'Position', 'Month', 'Working Hours']]
        
        final_summary = combined_df.groupby(['EmployeeID', 'EmployeeName', 'Position', 'Month']).agg({'Working Hours': 'sum'}).reset_index()
        final_pivot_summary = final_summary.pivot_table(index=['EmployeeID', 'EmployeeName', 'Position'], columns='Month', values='Working Hours', fill_value=0).reset_index()
        st.write("Final Monthly Summary", final_pivot_summary)
        
        # Option to save the final summary to Excel
        if st.button("Save Final Summary to Excel"):
            final_pivot_summary.to_excel("final_attendance_summary.xlsx", index=False)
            st.success("Final summary saved to 'final_attendance_summary.xlsx'")
