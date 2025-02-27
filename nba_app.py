import pandas as pd
import streamlit as st

# Load CSV
df = pd.read_csv("nba_2025_per_game_stats.csv")

# Streamlit App
st.title("NBA 2025 Per Game Stats")
st.dataframe(df)  # Show the data

# Search for a player
player = st.text_input("Search for a player:")
if player:
    filtered_df = df[df["Player"].str.contains(player, case=False, na=False)]
    st.dataframe(filtered_df)