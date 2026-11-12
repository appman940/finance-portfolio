
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Active Equity Portfolio Lab",
    page_icon="📈",
    layout="wide",
)

st.title("Active Equity Portfolio Lab")
st.caption(
    "Fundamental Security Selection "
    "| Quantitative Portfolio Construction"
)

st.info(
    "Research prototype. All allocations are hypothetical "
    "and do not represent investment recommendations."
)

# Demonstration data: not live holdings
holdings = pd.DataFrame({
    "Ticker": ["MSFT", "GOOGL", "JPM", "V", "COST"],
    "Weight": [0.25, 0.20, 0.20, 0.20, 0.15],
    "Sector": [
        "Technology",
        "Communication Services",
        "Financials",
        "Financials",
        "Consumer Staples",
    ],
})

initial_capital = 100_000

col1, col2, col3 = st.columns(3)

col1.metric("Starting Capital", f"${initial_capital:,.0f}")
col2.metric("Number of Holdings", len(holdings))
col3.metric("Portfolio Allocation", f"{holdings['Weight'].sum():.0%}")

st.subheader("Portfolio Holdings")

display = holdings.copy()
display["Weight"] = display["Weight"].map(lambda x: f"{x:.1%}")
st.dataframe(display, hide_index=True, use_container_width=True)

st.subheader("Portfolio Allocation")

fig = px.pie(
    holdings,
    names="Ticker",
    values="Weight",
    hole=0.45,
    title="Illustrative Portfolio Weights",
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Sector Exposure")

sectors = holdings.groupby(
    "Sector", as_index=False
)["Weight"].sum()

fig_sector = px.bar(
    sectors,
    x="Sector",
    y="Weight",
    title="Sector Weights",
)

st.plotly_chart(fig_sector, use_container_width=True)

st.caption(
    "Next: historical prices, return calculations, "
    "benchmark comparison, and portfolio optimization."
)
