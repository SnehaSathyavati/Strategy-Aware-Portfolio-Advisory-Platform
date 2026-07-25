import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Strategy-Aware Portfolio Advisory Platform",
    page_icon="📈",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📈 Strategy-Aware Portfolio Advisory Platform")

st.write(
    """
    A quantitative portfolio advisory application that recommends 
    stocks based on investment strategy, market signals, and 
    analyst sentiment.
    """
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_stock_data():

    df = pd.read_csv(
        "data/latest_stock_features.csv"
    )

    return df


try:

    stock_data = load_stock_data()

    # TEMPORARY DEBUG
    


except Exception as e:

    st.error(
        f"Unable to load stock data.\n\nError: {e}"
    )

    st.stop()



# --------------------------------------------------
# SIDEBAR USER INPUT
# --------------------------------------------------

st.sidebar.header("Investor Preferences")


strategy = st.sidebar.selectbox(
    "Choose Investment Strategy",

    [
        "Growth",
        "Blue Chip",
        "Dividend Income",
        "Balanced"
    ]
)


investment_amount = st.sidebar.number_input(

    "Investment Amount (₹)",

    min_value=1000,

    value=50000,

    step=5000

)


number_of_stocks = st.sidebar.slider(

    "Number of Recommended Stocks",

    min_value=1,

    max_value=10,

    value=5

)

st.sidebar.markdown("---")
st.sidebar.subheader("Scenario Planner")

market_sentiment_shift = st.sidebar.slider(
    "Market Sentiment Shift (%)",
    min_value=-20,
    max_value=20,
    value=0,
    step=5
)

risk_tolerance = st.sidebar.select_slider(
    "Risk Tolerance",
    options=["Low", "Medium", "High"],
    value="Medium"
)

# --------------------------------------------------
# STRATEGY SCORING ENGINE
# --------------------------------------------------

def apply_strategy(df, strategy):


    data = df.copy()


    if strategy == "Growth":

        score_column = "Growth_Score"



    elif strategy == "Blue Chip":

        score_column = "BlueChip_Score"



    elif strategy == "Dividend Income":

        score_column = "Dividend_Score"



    elif strategy == "Small/Mid Cap":

        if "Growth_Score" in data.columns:

            score_column = "Growth_Score"

        else:

            score_column = data.columns[-1]



    else:

        # Balanced strategy

        available_scores = [

            col for col in [

                "Growth_Score",

                "BlueChip_Score",

                "Dividend_Score",

                "Sentiment_Score_scaled",

                "Trend_Score_scaled"

            ]

            if col in data.columns

        ]


        data["Balanced_Score"] = (
            data[available_scores]
            .mean(axis=1)
        )


        score_column = "Balanced_Score"



    ranked = (

        data.sort_values(

            by=score_column,

            ascending=False

        )

        .head(number_of_stocks)

    )


    return ranked, score_column




# --------------------------------------------------
# SCENARIO PLANNER
# --------------------------------------------------

scenario_data = stock_data.copy()

# Adjust analyst sentiment
scenario_data["Sentiment_Score_scaled"] = (
    scenario_data["Sentiment_Score_scaled"] *
    (1 + market_sentiment_shift / 100)
)

scenario_data["Sentiment_Score_scaled"] = (
    scenario_data["Sentiment_Score_scaled"]
    .clip(0, 1)
)

# Adjust volatility according to risk tolerance
if risk_tolerance == "Low":

    scenario_data["Volatility_scaled"] = (
        scenario_data["Volatility_scaled"] * 1.25
    )

elif risk_tolerance == "High":

    scenario_data["Volatility_scaled"] = (
        scenario_data["Volatility_scaled"] * 0.75
    )

scenario_data["Volatility_scaled"] = (
    scenario_data["Volatility_scaled"]
    .clip(0, 1)
)

# Recalculate strategy scores

scenario_data["Growth_Score"] = (
    0.5 * scenario_data["Momentum_30_scaled"] +
    0.3 * scenario_data["Sentiment_Score_scaled"] +
    0.2 * scenario_data["Trend_Score_scaled"]
)

scenario_data["BlueChip_Score"] = (
    0.4 * (1 - scenario_data["Volatility_scaled"]) +
    0.3 * scenario_data["Sentiment_Score_scaled"] +
    0.3 * scenario_data["Trend_Score_scaled"]
)

scenario_data["Dividend_Score"] = (
    0.5 * (1 - scenario_data["Volatility_scaled"]) +
    0.2 * scenario_data["Sentiment_Score_scaled"] +
    0.3 * scenario_data["Trend_Score_scaled"]
)

# --------------------------------------------------
# STOCK EXPLAINABILITY
# --------------------------------------------------

def explain_stock(row, strategy):

    reasons = []

    if row["Momentum_30_scaled"] > 0.6:
        reasons.append("High Momentum")

    if row["Sentiment_Score_scaled"] > 0.6:
        reasons.append("Positive Analyst Sentiment")

    if row["Trend_Score_scaled"] > 0.5:
        reasons.append("Strong Upward Trend")

    if row["Volatility_scaled"] < 0.4:
        reasons.append("Low Volatility")

    # Strategy-specific fallback
    if strategy == "Growth" and not reasons:
        reasons.append("Balanced Growth Indicators")

    elif strategy == "Blue Chip" and not reasons:
        reasons.append("Stable Market Performance")

    elif strategy == "Dividend Income" and not reasons:
        reasons.append("Stable Income Characteristics")

    return ", ".join(reasons)

# Generate recommendations

recommendations, score_column = apply_strategy(
    scenario_data,
    strategy
)



# --------------------------------------------------
# DISPLAY USER SELECTION
# --------------------------------------------------

st.subheader("Investor Selection")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Strategy",
        strategy
    )


with col2:

    st.metric(
        "Investment",
        f"₹{investment_amount:,}"
    )


with col3:

    st.metric(
        "Stocks Selected",
        number_of_stocks
    )
st.info(
    f"""
### 🎯 Current Scenario

📈 **Market Sentiment Shift:** {market_sentiment_shift:+d}%

⚖️ **Risk Tolerance:** {risk_tolerance}
"""
)


# --------------------------------------------------
# RECOMMENDED STOCKS
# --------------------------------------------------

st.subheader(
    "⭐ Recommended Stocks"
)


display_columns = [
    "Ticker",
    "Why this Stock?"
]


for col in [

    score_column,

    "Sentiment_Score_scaled",

    "Trend_Score_scaled",

    "Close"

]:

    if col in recommendations.columns:

        display_columns.append(col)

recommendations["Why this Stock?"] = recommendations.apply(
    lambda row: explain_stock(row, strategy),
    axis=1
)


st.dataframe(

    recommendations[display_columns],

    use_container_width=True

)



# --------------------------------------------------
# PORTFOLIO ALLOCATION
# --------------------------------------------------

st.subheader(
    "💰 Suggested Portfolio Allocation"
)


portfolio = recommendations.copy()

# Normalize scores to create weights
portfolio["Weight (%)"] = (
    portfolio[score_column] /
    portfolio[score_column].sum()
) * 100

# Allocate investment based on weights
portfolio["Investment_Amount"] = (
    investment_amount *
    portfolio["Weight (%)"] / 100
)

# Round values
portfolio["Weight (%)"] = portfolio["Weight (%)"].round(2)
portfolio["Investment_Amount"] = portfolio["Investment_Amount"].round(2)



st.dataframe(

    portfolio[

        [

            "Ticker",

            "Investment_Amount",

            "Weight (%)"

        ]

    ],

    use_container_width=True

)



# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------


st.subheader(
    "📊 Strategy Ranking"
)



fig = px.bar(

    recommendations,

    x="Ticker",

    y=score_column,

    title=f"{strategy} Stock Ranking"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# --------------------------------------------------
# SENTIMENT ANALYSIS
# --------------------------------------------------

if "Sentiment_Score_scaled" in recommendations.columns:


    st.subheader(
        "📰 Analyst Sentiment"
    )


    sentiment_chart = px.bar(

        recommendations,

        x="Ticker",

        y="Sentiment_Score_scaled",

        title="Sentiment Score"

    )


    st.plotly_chart(

        sentiment_chart,

        use_container_width=True

    )



# --------------------------------------------------
# PORTFOLIO SUMMARY
# --------------------------------------------------

st.subheader(
    "📌 Portfolio Summary"
)


total_invested = portfolio["Investment_Amount"].sum()



col1, col2 = st.columns(2)


with col1:

    st.metric(

        "Total Investment",

        f"₹{total_invested:,.0f}"

    )


with col2:

    st.metric(

        "Number of Holdings",

        len(portfolio)

    )

st.subheader("💧 Portfolio Value Waterfall (Illustrative)")

starting_value = investment_amount

# Simple illustrative assumptions
estimated_market_gain = starting_value * 0.08
estimated_dividend = starting_value * 0.02
estimated_fees = -(starting_value * 0.005)

fig = go.Figure(
    go.Waterfall(
        name="Portfolio",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=[
            "Starting Investment",
            "Market Gain",
            "Dividend",
            "Fees",
            "Estimated Final Value"
        ],
        y=[
            starting_value,
            estimated_market_gain,
            estimated_dividend,
            estimated_fees,
            0
        ],
    )
)

fig.update_layout(
    title="Illustrative Portfolio Value Breakdown",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "This chart illustrates a hypothetical scenario using simple assumptions. "
    "It is not a forecast of future investment performance."
)

st.success(
    "Recommendation generated successfully!"
)