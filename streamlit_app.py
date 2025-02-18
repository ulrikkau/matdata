import streamlit as st

st.title("🎈Min mat")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

import pandas as pd
from datetime import datetime

# Load or create your food database
food_db = pd.read_csv("LivsmedelsDB_202502172001.csv")

# Create input fields
food_item = st.selectbox("Select food item", food_db["Food"].tolist())
amount = st.number_input("Amount (g)", min_value=0.0, step=0.1)
date_time = st.date_input("Date") + " " + st.time_input("Time").strftime("%H:%M:%S")

# Add custom food option
custom_food = st.text_input("Or add a custom food item")
custom_calories = st.number_input("Calories per 100g", min_value=0)

if st.button("Log Food"):
    # Log the food item with date and time
    # Add to your database or CSV file
    st.success("Food logged successfully!")

# Display logged foods
st.write("Your food log:")
# Retrieve and display the food log
