#app.py
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Define the database file path
DB_FILE = "food_log.db"

# Function to create the database and table if they don't exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS food_log
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  food_item TEXT,
                  amount REAL,
                  date_time TEXT)''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Streamlit app
def main():
    st.title("Food Logger")

    # Input fields
    food_item = st.text_input("Food Item")
    amount = st.number_input("Amount (g)", min_value=0.0, step=0.1)
    
    # Date and time input
    date = st.date_input("Date")
    time = st.time_input("Time")
    
    # Combine date and time into a single datetime object
    date_time = datetime.combine(date, time)

    if st.button("Log Food"):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO food_log (food_item, amount, date_time) VALUES (?, ?, ?)",
                  (food_item, amount, date_time.strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        st.success("Food logged successfully!")

    # Display logged foods
    st.write("Your food log:")
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM food_log", conn)
    st.dataframe(df)
    conn.close()

if __name__ == "__main__":
    main()
