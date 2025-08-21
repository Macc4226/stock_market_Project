import streamlit as st
import pandas as pd
from utils import StockData

# Intitializing Streamlit app
st.set_page_config(page_title="Stock Market Project", layout="wide")


@st.cache_resource(ttl=3600)
def get_client():
    return StockData()


# Get the client
client = get_client()


# Symbol search function
@st.cache_data(ttl=3600, hash_funcs={pd.DataFrame: lambda x: None})
def sym_search(company: str) -> pd.DataFrame:
    search = client.symbol_search(company)
    return search


# Add title on the page
st.title("Stock Market API project")

# Add subheader author name
st.subheader("by Utkarsh Gaikwad")

# Take company name as text input from user
company = st.text_input("Enter Company Name : ")

# If company name is entered
if company:
    # Search for company symbols
    search = sym_search(company)
    st.dataframe(search)

    # Once search results are there create a dropdown to select symbol
    selected_symbol = st.selectbox(
        "Select the symbol", options=search["1. symbol"].tolist()
    )

    # Create a button to plot the results
    button = st.button(label="plot", type="primary")

    # If button is pressed plot the results
    if button:
        df = client.get_daily_data(selected_symbol)
        fig = client.plot_chart(df)
        st.plotly_chart(fig)