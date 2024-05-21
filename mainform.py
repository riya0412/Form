import streamlit as st

# Sidebar for navigation
st.sidebar.title("Form Navigation")
option = st.sidebar.selectbox("Choose a form to display", ["Attendance Form", "Unloading Form", "Loading Form"])

# Display the selected form
if option == "Attendance Form":
    st.title("Attendance Form")
    exec(open("Attendance.py").read())
elif option == "Unloading Form":
    st.title("Unloading Form")
    exec(open("Unloading.py").read())
elif option == "Loading Form":
    st.title("Loading Form")
    exec(open("Loading.py").read())
