import streamlit as st
from utils import StockData # Import the class from your utils.py file

# --- Streamlit App UI ---
st.set_page_config(layout="wide")
st.title("📈 Stock Analysis Dashboard")
st.write("This app retrieves and displays stock data using the Alpha Vantage API.")

# Instantiate the data handler class
stock_data_handler = StockData()

# 1. User input for company search
company_name = st.text_input("Enter a company name to find its stock symbol:", "Tesla")

if company_name:
    # 2. Search for symbols and let the user select one
    search_results = stock_data_handler.symbol_search(company_name)

    if not search_results.empty:
        search_results["display"] = search_results["1. symbol"] + " - " + search_results["2. name"] + " (" + search_results["4. region"] + ")"
        
        selected_stock = st.selectbox(
            "Select a stock from the search results:",
            options=search_results["display"]
        )
        
        if selected_stock:
            selected_symbol = selected_stock.split(" - ")[0]
            st.subheader(f"Displaying data for: {selected_symbol}")

            # 3. Get and display the daily data and chart
            daily_data = stock_data_handler.get_daily_data(selected_symbol)

            if not daily_data.empty:
                fig = stock_data_handler.plot_chart(daily_data, selected_symbol)
                st.plotly_chart(fig, use_container_width=True)

                with st.expander("View Raw Data"):
                    st.dataframe(daily_data)
            else:
                st.warning("No data could be displayed for the selected symbol.")
    else:
        st.info("No results found for your search. Please try another company name.")