import streamlit as st
import Attendance
import Unloading
import Loading

st.set_page_config(page_title="Main Dashboard", page_icon=":house:", layout="wide")

def main():
    # CSS for better styling
    st.markdown("""
        <style>
            .main-title {
                font-size: 3em;
                color: #4CAF50;
                text-align: center;
            }
            .sidebar .sidebar-content {
                background-color: #f4f4f4;
            }
            .sidebar .sidebar-content .element-container {
                margin-bottom: 10px;
            }
            .quick-links {
                margin-top: 50px;
                text-align: center;
            }
            .quick-links a {
                text-decoration: none;
                color: #007BFF;
                font-size: 1.2em;
                margin: 0 10px;
            }
            .quick-links a:hover {
                color: #0056b3;
                text-decoration: underline;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">Main Dashboard</h1>', unsafe_allow_html=True)
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Choose a form to fill:")

    # Dictionary of pages
    pages = {
        "Attendance Form": Attendance,
        "Unloading Form": Unloading,
        "Loading Form": Loading
    }

    # Sidebar radio buttons for navigation
    page = st.sidebar.radio("Go to", list(pages.keys()))

    # Load the selected page
    pages[page].app()

    # Display links to other forms in the main area
    st.markdown('<div class="quick-links">### Quick Links</div>', unsafe_allow_html=True)
    st.markdown('<div class="quick-links"><a href="D:/Kuber Inventory/FORMS/Attendance.py" onclick="window.open(\'D:/Kuber Inventory/FORMS/Attendance.py\', \'_blank\')">Attendance Form</a></div>', unsafe_allow_html=True)
    st.markdown('<div class="quick-links"><a href="D:/Kuber Inventory/FORMS/Unloading.py" onclick="window.open(\'D:/Kuber Inventory/FORMS/Unloading.py\', \'_blank\')">Unloading Form</a></div>', unsafe_allow_html=True)
    st.markdown('<div class="quick-links"><a href="D:/Kuber Inventory/FORMS/Loading.py" onclick="window.open(\'D:/Kuber Inventory/FORMS/Loading.py\', \'_blank\')">Loading Form</a></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
