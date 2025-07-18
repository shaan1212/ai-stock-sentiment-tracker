# app.py

import yfinance as yf
from textblob import TextBlob
import streamlit as st
import plotly.graph_objects as go
import requests

# --- Functions ---

def get_stock_data(ticker="AAPL"):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1d", interval="1m")
    return df[['Close']]

def get_news_sentiment(query="Apple"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey=YOUR_NEWSAPI_KEY"
    response = requests.get(url).json()
    scores = []
    if 'articles' in response:
        for article in response['articles'][:5]:
            text = article['title'] + " " + article.get('description', '')
            sentiment = TextBlob(text).sentiment.polarity
            scores.append(sentiment)
    return sum(scores)/len(scores) if scores else 0

def generate_signal(sentiment, trend_now, trend_before):
    if sentiment > 0.2 and trend_now > trend_before:
        return "BUY 📈"
    elif sentiment < -0.2 and trend_now < trend_before:
        return "SELL 📉"
    else:
        return "HOLD 🤝"

# --- Streamlit App UI ---

st.title("📊 AI Stock Sentiment + Trend Tracker")

ticker = st.text_input("Enter Stock Symbol (e.g. AAPL, TSLA):", "AAPL")
query = ticker

df = get_stock_data(ticker)
sentiment = get_news_sentiment(query)
signal = generate_signal(sentiment, df['Close'].iloc[-1], df['Close'].iloc[-5])

st.write(f"**Sentiment Score**: {sentiment:.2f}")
st.write(f"**Trading Signal**: {signal}")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'))
st.plotly_chart(fig)
url = f"https://newsapi.org/v2/everything?q={query}&apiKey=d2d330181e9242c6a220656fd22397db"