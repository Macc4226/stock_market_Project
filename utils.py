import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go


class StockData:

    def __init__(self):
        api_key = st.secrets["API_KEY"]
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com",
        }
    @st.cache_data(ttl=3600)
    def symbol_search(self, company: str):
        querystring = {
            "datatype": "json",
            "keywords": company,
            "function": "SYMBOL_SEARCH",
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        search = response.json()["bestMatches"]
        search_df = pd.DataFrame(search)
        return search_df

    @st.cache_data(ttl=3600)
    def get_daily_data(self, symbol: str):
        querystring = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact",
            "datatype": "json",
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        daily = response.json()["Time Series (Daily)"]
        daily_df = pd.DataFrame(daily).T
        daily_df = daily_df.astype(float)
        daily_df.index = pd.to_datetime(daily_df.index)
        daily_df.index.name = "date"
        return daily_df

    def plot_chart(self, data: pd.DataFrame):
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data.index,
                    open=data["1. open"],
                    high=data["2. high"],
                    low=data["3. low"],
                    close=data["4. close"],
                )
            ]
        )
        fig.update_layout(width=1200, height=800)
        return fig
