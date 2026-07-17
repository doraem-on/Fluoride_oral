
import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="OralAtlas 2026 Dashboard", layout="wide")
st.title("🦷 OralAtlas 2026: Global Oral Care Intelligence")

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'exports', 'oralatlas.db')

@st.cache_data
def load_data(query):
    if not os.path.exists(db_path):
        return pd.DataFrame()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.markdown("Welcome to the interactive explorer for the OralAtlas 2026 dataset.")
