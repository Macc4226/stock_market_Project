import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

class StockData:
    """
    A class to fetch, process, and visualize stock data from the Alpha Vantage API.
    """
    def __init__(self):
        try:
            api_key = st.secrets["API_KEY"]
        except (KeyError, FileNotFoundError):
            st.error("API_KEY not found in Streamlit secrets. Please add it to your secrets file.")
            st.stop()

        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com",
        }

    @st.cache_data(ttl=3600)
    def symbol_search(self, company: str):
        querystring = {"datatype": "json", "keywords": company, "function": "SYMBOL_SEARCH"}
        try:
            response = requests.get(self.url, headers=self.headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            if "bestMatches" in data:
                return pd.DataFrame(data["bestMatches"])
            else:
                st.warning(f"Could not find any stock symbols for '{company}'.")
                return pd.DataFrame()
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred during API request: {e}")
            return pd.DataFrame()

    @st.cache_data(ttl=3600)
    def get_daily_data(self, symbol: str):
        querystring = {"function": "TIME_SERIES_DAILY", "symbol": symbol, "outputsize": "compact", "datatype": "json"}
        try:
            response = requests.get(self.url, headers=self.headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            if "Time Series (Daily)" in data:
                daily_df = pd.DataFrame(data["Time Series (Daily)"]).T
                daily_df = daily_df.astype(float)
                daily_df.index = pd.to_datetime(daily_df.index)
                daily_df.index.name = "date"
                return daily_df
            else:
                st.warning(f"Could not retrieve daily data for symbol '{symbol}'.")
                return pd.DataFrame()
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred during API request: {e}")
            return pd.DataFrame()

    def plot_chart(self, data: pd.DataFrame, symbol: str):
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data["1. open"], high=data["2. high"], low=data["3. low"], close=data["4. close"])])
        fig.update_layout(title=f'{symbol} Daily Candlestick Chart', xaxis_title='Date', yaxis_title='Price (USD)', xaxis_rangeslider_visible=False)
        return fig