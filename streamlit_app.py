import streamlit as st

st.title("🎈Min mat")

import pandas as pd
import sqlite3
from datetime import datetime , timedelta
from io import BytesIO
import xlsxwriter

# Define the database file path
DB_FILE = "food_log.db"

def get_all_data_from_db():
    conn = sqlite3.connect(DB_FILE)
    query = "SELECT * FROM food_log ORDER BY date_time ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = get_all_data_from_db()
df['date_time'] = pd.to_datetime(df['date_time'])

min_date = df['date_time'].min().date()
max_date = df['date_time'].max().date()
start_date = st.date_input("Start Date", min_date)
end_date = st.date_input("End Date", max_date)


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
def get_food_items():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT DISTINCT food_item FROM food_log ORDER BY food_item ASC")
    items = [item[0] for item in c.fetchall()]
    conn.close()
    return items

existing_food_items = get_food_items()


if st.button("Download Excel"):
    filtered_df = df[(df['date_time'].dt.date >= start_date) & (df['date_time'].dt.date <= end_date)]
    excel_data = to_excel(filtered_df)
    st.download_button(
        label="📥 Download Excel file",
        data=excel_data,
        file_name="food_log.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Streamlit app
def main():
    st.title("Food Logger")
    # Fetch existing food items
    existing_food_items = get_food_items()

    # Input fields
    food_item = st.selectbox("Food Item", options=[""] + existing_food_items, index=0)
    if food_item == "":
        food_item = st.text_input("Enter a new food item")

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
    
    df = pd.read_sql_query("SELECT * FROM food_log ORDER BY date_time DESC", conn)

    st.dataframe(df)
    conn.close()



if __name__ == "__main__":
    main()
