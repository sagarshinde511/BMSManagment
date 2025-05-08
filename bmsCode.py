import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Database configuration
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students",
    "password": "testStudents@123",
    "database": "u263681140_students"
}

# Default login credentials
USERNAME = "admin"
PASSWORD = "123"

# Function to authenticate user
def login(username, password):
    return username == USERNAME and password == PASSWORD

# Function to fetch data from database
def fetch_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT * FROM BMS1"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit App
def main():
    st.title("🔋 BMS Monitoring System")

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Login
    if not st.session_state.logged_in:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            if login(username, password):
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials!")

    # Logged-in view
    if st.session_state.logged_in:
        # Logout
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        st.success("You are logged in!")

        # Tabs
        tab1, tab2 = st.tabs(["📊 BMS1 Dashboard", "🛠️ Tab 2 Placeholder"])

        with tab1:
            st.subheader("Fetched Data Table 📄")
            df = fetch_data()
            st.dataframe(df)

            # Convert data types
            df['temp'] = pd.to_numeric(df['temp'], errors='coerce')
            df['vtg'] = pd.to_numeric(df['vtg'], errors='coerce')
            df['current'] = pd.to_numeric(df['current'], errors='coerce')

            # Adjust voltage
            df['vtg'] = df['vtg'] / 2

            # Graphs
            st.subheader("Temperature Over Time 🌡️")
            fig1 = px.line(df, x='dateTime', y='temp', title='Temperature Over Time')
            st.plotly_chart(fig1)

            st.subheader("Voltage Over Time ⚡")
            fig2 = px.line(df, x='dateTime', y='vtg', title='Voltage Over Time')
            st.plotly_chart(fig2)

            st.subheader("Current Over Time 🔌")
            fig3 = px.line(df, x='dateTime', y='current', title='Current Over Time')
            st.plotly_chart(fig3)

        with tab2:
            st.subheader("Analyse Data")
            st.write("Redirecting to Analyse Data...")
            st.markdown('<a href="https://bmsgcek-5vwhdph3tjqhgfzstsmt6gcek.streamlit.app///" target="_blank">Click here if not redirected</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
