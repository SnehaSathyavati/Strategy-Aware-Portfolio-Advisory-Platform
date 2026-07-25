# 📈 Strategy-Aware Portfolio Advisory Platform

A quantitative finance and data science application that recommends personalized stock portfolios based on investment strategy, market indicators, and analyst sentiment.

Built using **Python**, **Pandas**, **Plotly**, and **Streamlit**, this project demonstrates how financial analytics and data-driven decision-making can be combined into an interactive portfolio advisory application.

---

# 🚀 Project Overview

Investors often need to compare multiple stocks using historical performance, market trends, volatility, and analyst opinions before making investment decisions.

This project addresses that challenge by building a **Strategy-Aware Portfolio Advisory Platform** that analyzes financial data, calculates strategy-specific scores, and recommends personalized portfolios based on the investor's preferences.

Unlike traditional stock screeners, the application adapts recommendations according to different investment strategies and allows users to perform simple scenario analysis.

The platform is designed as a **decision-support tool** for educational and analytical purposes. It does **not** execute trades or provide financial advice.

---

# 🎯 Objectives

- Analyze historical stock market data.
- Generate financial indicators through feature engineering.
- Incorporate analyst sentiment into stock evaluation.
- Recommend stocks using strategy-specific scoring models.
- Construct a score-weighted investment portfolio.
- Provide an interactive dashboard for portfolio exploration.

---

# ✨ Features

### 📊 Financial Data Analysis

- Historical stock price analysis
- Daily return calculation
- Moving averages (MA20 & MA50)
- Volatility analysis
- Momentum calculation

---

### 📈 Strategy-Based Recommendation Engine

Supports four investment strategies:

- Growth Investing
- Blue Chip Investing
- Dividend Income Investing
- Balanced Portfolio

Each strategy uses a customized scoring model based on financial indicators and analyst sentiment.

---

### 😊 Analyst Sentiment Integration

The recommendation engine incorporates analyst recommendation data to improve stock evaluation.

Sentiment scores are normalized and combined with technical indicators.

---

### ⚖️ Score-Weighted Portfolio Allocation

Instead of allocating equal investment to every stock, the application distributes investment proportionally according to the calculated strategy scores.

---

### 🎛️ Scenario Planner

Users can simulate different investment scenarios by adjusting:

- Market Sentiment Shift
- Risk Tolerance
- Investment Amount

Recommendations and portfolio allocation update dynamically based on the selected scenario.

---

### 💡 Explainable Recommendations

Each recommended stock includes a short explanation describing the key factors influencing its recommendation, improving transparency and interpretability.

---

### 📊 Interactive Visualizations

The dashboard includes:

- Strategy Ranking Chart
- Analyst Sentiment Chart
- Portfolio Allocation
- Portfolio Summary
- Waterfall Chart (Illustrative)

---

# 🧠 Methodology

The project follows an end-to-end data science workflow:

```
Historical Stock Data
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Analyst Sentiment Integration
        │
        ▼
Feature Scaling
        │
        ▼
Strategy Scoring
        │
        ▼
Scenario Analysis
        │
        ▼
Stock Ranking
        │
        ▼
Portfolio Allocation
        │
        ▼
Interactive Dashboard
```

---

# 🛠 Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib |
| Machine Learning | Scikit-learn |
| Financial Data | yFinance |
| Dashboard | Streamlit |
| Development | Jupyter Notebook, VS Code |

---

# 📁 Project Structure

```
strategy-aware-portfolio-advisory-platform/

│
├── data/
│   ├── latest_stock_features.csv
│   ├── sentiment_data.csv
│   └── stock_prices.csv
│
├── notebooks/
│   └── Strategy_Aware_Portfolio_Advisory_Platform.ipynb
│
├── outputs/
│   ├── recommended_portfolio.csv
│   ├── performance_metrics.csv
│   ├── portfolio_summary.csv
│   └── portfolio_vs_benchmark.png
│
├── src/
│   └── app.py
│
├── images/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# ▶️ Running the Project

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/strategy-aware-portfolio-advisory-platform.git
```

---

## 2. Navigate to the project

```bash
cd strategy-aware-portfolio-advisory-platform
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Launch the application

```bash
streamlit run src/app.py
```

---

# 📷 Dashboard Preview

Add screenshots here after uploading them.

Example:

```
images/dashboard.png
images/scenario_planner.png
images/portfolio_allocation.png
images/waterfall_chart.png
```

---

# 📊 Example Output

The application provides:

- Personalized stock recommendations
- Strategy ranking scores
- Portfolio allocation
- Analyst sentiment visualization
- Portfolio summary
- Scenario analysis

---

# ⚠️ Limitations

- Uses historical market data and analyst sentiment for analysis.
- Recommendations are based on heuristic scoring models rather than predictive machine learning.
- The waterfall chart is illustrative and does not represent actual future investment performance.
- The project currently evaluates a selected universe of stocks.

---

# 🚀 Future Improvements

Possible future enhancements include:

- Live market data streaming
- Additional investment strategies
- ETF and mutual fund support
- Portfolio optimization using advanced optimization techniques
- Backtesting framework
- Risk-adjusted performance metrics
- Cloud deployment

---

# 👩‍💻 Author

**Sneha A**

Data Analyst | Data Science | Financial Analytics

LinkedIn:
(Add your LinkedIn URL)

GitHub:
(Add your GitHub URL)

---

# 📄 License

This project is licensed under the MIT License.

---

## ⭐ If you found this project useful, consider giving it a star!

# 📷 Dashboard Preview

## Main Dashboard

![Dashboard](images/dashboard.png)

## Portfolio Allocation & Strategy Ranking

![Portfolio Allocation](images/allocation.png)

## Analyst Sentiment

![Analyst Sentiment](images/sentiment.png)

## Portfolio Value Waterfall

![Waterfall](images/waterfall.png)