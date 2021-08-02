from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import datetime
import plotly.express as px

#Method to Scrape Wikepedia and the results are stored "@st.cache" so that we do not have to scrape everytime a change is made
@st.cache
def scrape_sp500_wiki():

    url_companies = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    t_id = 'constituents'

    response = requests.get(url_companies)
    soup = BeautifulSoup(response.text, 'html.parser')
    sp500 =  soup.find('table', attrs={'id': t_id})
    df = pd.read_html(str(sp500))

    return df[0]


st.write("""
# Stock Price Prediction Project

Just a CS student trying something new!
""")

#Creating the Sidebar
st.sidebar.header("User Input")
text_box = st.sidebar.text_input("Enter the name of a the stock","")
st.sidebar.markdown(f"Stock: {text_box}")
st.sidebar.markdown(f"Enter the start and end dates for {text_box} historical data and the number of future days to forecast")
start_d = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_d = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))
number_days = st.sidebar.number_input('How many days in the future do you want to forecast?',min_value=1)

st.header("S&P 500 Wiki Table")
df = scrape_sp500_wiki()
st.dataframe(data=df, width=None, height=None)

stock = yf.Ticker(text_box)

try:
    stock_data = stock.history(period = "1d", start = start_d,end = end_d )
except:
    st.sidebar.markdown("Invalid tag input!")

try:
    if text_box:
        #Displaying Company info
        string_logo = '<img src=%s>' % stock.info['logo_url']
        st.markdown(string_logo, unsafe_allow_html=True)

        string_name = stock.info['longName']
        st.header('**%s**' % string_name)

        string_summary = stock.info['longBusinessSummary']
        st.info(string_summary)

        #Displaying the Historical Data
        st.header("Historical Data")
        st.dataframe(stock_data)
        stock_data_cleaned = stock_data[["Close"]]
        fig = px.line(stock_data_cleaned, x=stock_data_cleaned.index, y="Close", title='Historical Data Trend')
        st.write(fig)

        #Preparing the Data for analysis
        df_train = stock_data[["Close"]]
        df_train = df_train.reset_index(inplace=False)
        df_train = df_train.rename(columns={'Date':'ds','Close':'y'})

        """
        #Prediction
        st.header("Prediction")
        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=number_days)#(end_d - start_d).days)
        forecast = m.predict(future)
        st.header("Raw Forecast Data")
        st.dataframe(forecast)
        st.write("Forecasr Graph")
        fig1 = plot_plotly(m,forecast)
        st.plotly_chart(fig1)

        st.write('Forecast Components")
        fig2 = m.plot_componenets(forecast)
        st.write(fig2)
        """
except:
    st.sidebar.markdown("**Invalid tag input!**")

#df_train = stock_data[['Date','Close']]





#def plot_initial_data():







