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
PASSWORD = "password123"

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
    st.title("🔋 BMS1 Monitoring Dashboard")

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # If not logged in, show login form
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

    # If logged in, show dashboard
    if st.session_state.logged_in:
        # Logout button
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.ererun()

        st.success("You are logged in!")

        # Fetch and display data
        df = fetch_data()
        st.subheader("Fetched Data Table 📄")
        st.dataframe(df)

        # Convert columns to numeric
        df['temp'] = pd.to_numeric(df['temp'], errors='coerce')
        df['vtg'] = pd.to_numeric(df['vtg'], errors='coerce')
        df['current(mA)'] = pd.to_numeric(df['current(mA)'], errors='coerce')

        # ⚡ Divide voltage by 2
        df['vtg'] = df['vtg'] / 2

        # Plotting graphs
        st.subheader("Temperature Over Time 🌡️")
        fig1 = px.line(df, x='dateTime', y='temp', title='Temperature Over Time')
        st.plotly_chart(fig1)

        st.subheader("Voltage Over Time (Divided by 2) ⚡")
        fig2 = px.line(df, x='dateTime', y='vtg', title='Voltage Over Time')
        st.plotly_chart(fig2)

        st.subheader("Current (mV) Over Time 🔌")
        fig3 = px.line(df, x='dateTime', y='current(mA)', title='Current (mV) Over Time')
        st.plotly_chart(fig3)

if __name__ == "__main__":
    main()

