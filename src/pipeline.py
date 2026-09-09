import os
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

FINNHUB_API_KEY = os.environ["FINNHUB_API_KEY"]  # set via .env / st.secrets, never hardcoded

DEFAULT_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "NVDA", "TSLA", "JPM", "V", "JNJ",
]


# --------------------------------------------------
# DATA DOWNLOAD
# --------------------------------------------------

def download_price_data(tickers, start_date, end_date):
    """Download OHLCV data for a list of tickers and return a tidy long-format DataFrame."""
    raw = yf.download(tickers, start=start_date, end=end_date, group_by="ticker")
    tidy = raw.stack(level=0).reset_index()
    tidy.columns = ["Date", "Ticker", "Close", "High", "Low", "Open", "Volume"]
    return tidy


def fetch_analyst_sentiment(tickers, api_key=None):
    """Fetch analyst recommendation sentiment scores from Finnhub for each ticker."""
    api_key = api_key or FINNHUB_API_KEY
    records = []
    for ticker in tickers:
        url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={ticker}&token={api_key}"
        response = requests.get(url)
        data = response.json()
        if not data:
            continue
        latest = data[0]
        total = latest["strongBuy"] + latest["buy"] + latest["hold"] + latest["sell"] + latest["strongSell"]
        score = 0 if total == 0 else (
            (2 * latest["strongBuy"]) + latest["buy"] - latest["sell"] - (2 * latest["strongSell"])
        ) / total
        records.append({"Ticker": ticker, "Sentiment_Score": score})
    return pd.DataFrame(records)


# --------------------------------------------------
# FEATURE ENGINEERING
# --------------------------------------------------

def engineer_features(price_df, sentiment_df):
    """Merge sentiment and compute returns, moving averages, momentum, volatility, trend."""
    df = price_df.merge(sentiment_df, on="Ticker", how="left")

    df["Returns"] = df.groupby("Ticker")["Close"].pct_change()
    df["MA20"] = df.groupby("Ticker")["Close"].transform(lambda x: x.rolling(20).mean())
    df["MA50"] = df.groupby("Ticker")["Close"].transform(lambda x: x.rolling(50).mean())
    df["Momentum_30"] = df.groupby("Ticker")["Close"].pct_change(periods=30)
    df["Volatility"] = df.groupby("Ticker")["Returns"].transform(lambda x: x.rolling(30).std())
    df["Trend_Score"] = (df["MA20"] > df["MA50"]).astype(int) * 2

    return df.dropna().reset_index(drop=True)


def scale_features(df):
    """Min-max scale the raw features used for scoring."""
    features = ["Momentum_30", "Volatility", "Sentiment_Score", "Trend_Score"]
    scaled_cols = [f"{f}_scaled" for f in features]
    scaler = MinMaxScaler()
    df[scaled_cols] = scaler.fit_transform(df[features])
    return df


# --------------------------------------------------
# STRATEGY SCORING
# --------------------------------------------------

# Weights are named and centralized here so they're easy to find, cite, and vary
# (e.g. for the sensitivity check) rather than being buried inline.
STRATEGY_WEIGHTS = {
    "Growth":   {"Momentum_30_scaled": 0.5, "Sentiment_Score_scaled": 0.3, "Trend_Score_scaled": 0.2},
    "BlueChip": {"InvVolatility":      0.4, "Sentiment_Score_scaled": 0.3, "Trend_Score_scaled": 0.3},
    "Dividend": {"InvVolatility":      0.5, "Sentiment_Score_scaled": 0.2, "Trend_Score_scaled": 0.3},
}


def compute_strategy_scores(df, weights=None):
    """Compute Growth/BlueChip/Dividend scores using a (possibly overridden) weight set."""
    weights = weights or STRATEGY_WEIGHTS
    df = df.copy()
    df["InvVolatility"] = 1 - df["Volatility_scaled"]

    df["Growth_Score"] = sum(df[col] * w for col, w in weights["Growth"].items())
    df["BlueChip_Score"] = sum(df[col] * w for col, w in weights["BlueChip"].items())
    df["Dividend_Score"] = sum(df[col] * w for col, w in weights["Dividend"].items())

    return df


def get_latest_features(df):
    """Return only the most recent trading day's rows — the snapshot the app consumes."""
    return df[df["Date"] == df["Date"].max()]


# --------------------------------------------------
# FULL PIPELINE
# --------------------------------------------------

def run_pipeline(tickers=None, start_date="2020-01-01", end_date=None):
    """End-to-end: download -> sentiment -> features -> scale -> score -> latest snapshot."""
    tickers = tickers or DEFAULT_TICKERS
    end_date = end_date or pd.Timestamp.today().strftime("%Y-%m-%d")

    prices = download_price_data(tickers, start_date, end_date)
    sentiment = fetch_analyst_sentiment(tickers)
    features = engineer_features(prices, sentiment)
    scaled = scale_features(features)
    scored = compute_strategy_scores(scaled)
    latest = get_latest_features(scored)

    return latest
if __name__ == "__main__":
    result = run_pipeline()
    print(result.head())


if __name__ == "__main__":
    result = run_pipeline()
    result.to_csv("Data/latest_stock_features.csv", index=False)
    print(result.head())
