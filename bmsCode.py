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

# --- Default login credentials ---
USERNAME = "admin"
PASSWORD = "password123"

# --- Function to authenticate user ---
def login(username, password):
    return username == USERNAME and password == PASSWORD

# --- Function to fetch data from database ---
def fetch_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT * FROM BMS1"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- Streamlit App ---
def main():
    st.title("BMS1 Monitoring Dashboard")

    # Login
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if login(username, password):
            st.success("Logged in successfully!")

            # Fetch and display data
            df = fetch_data()
            st.subheader("Fetched Data")
            st.dataframe(df)

            # Convert temp, vtg, and current(mV) to numeric (in case stored as text)
            df['temp'] = pd.to_numeric(df['temp'], errors='coerce')
            df['vtg'] = pd.to_numeric(df['vtg'], errors='coerce')
            df['current(mV)'] = pd.to_numeric(df['current(mV)'], errors='coerce')

            # Plotting graphs
            st.subheader("Temperature Over Time")
            fig1 = px.line(df, x='dateTime', y='temp', title='Temperature Over Time')
            st.plotly_chart(fig1)

            st.subheader("Voltage Over Time")
            fig2 = px.line(df, x='dateTime', y='vtg', title='Voltage Over Time')
            st.plotly_chart(fig2)

            st.subheader("Current (mV) Over Time")
            fig3 = px.line(df, x='dateTime', y='current(mV)', title='Current (mV) Over Time')
            st.plotly_chart(fig3)

        else:
            st.error("Invalid credentials!")

if __name__ == "__main__":
    main()
