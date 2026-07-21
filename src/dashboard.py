"""DistillateDesk dashboard — pass 1: prices.

Run from the repo root:
    streamlit run src/dashboard.py
"""
from __future__ import annotations
import altair as alt

import pandas as pd
import streamlit as st

import analytics
import config
import curve as cv

st.set_page_config(page_title="DistillateDesk", layout="wide")


def diesel_jet_spread_zscore(prices: pd.DataFrame) -> pd.Series:
    diesel_jet = diesel_jet_spread(prices)
    return analytics.zscore(diesel_jet)

def diesel_jet_spread(prices: pd.DataFrame) -> pd.Series:
    dieselbbl = analytics.gallons_to_barrel(prices["diesel"])
    jetbbl = analytics.gallons_to_barrel(prices["jet_fuel"])
    return analytics.diesel_jet_spread(dieselbbl, jetbbl)

@st.cache_data
def load_prices() -> pd.DataFrame:
    return pd.read_parquet(config.PRICES_FILE)

@st.cache_data(ttl=3600)
def load_curve(root: str, months: int) -> pd.DataFrame:
    return cv.curve_snapshot(root, months)

n_months = st.sidebar.slider(
    "Curve length (contracts)",
    min_value=2, max_value=12, value=6,
)

curve = load_curve("HO", n_months)


st.title("Distillate Desk")
st.caption("Middle distillates, prices, cracks and spreads")

try:
    prices = load_prices()
except FileNotFoundError:
    st.warning("No data yet. Run `python -m src.ingest` first.")
    st.stop()

in_bbl = pd.DataFrame({
    "Brent crude": prices["brent"],
    "Heating oil": analytics.gallons_to_barrel(prices["heating_oil"]),
    "Diesel":      analytics.gallons_to_barrel(prices["diesel"]),
    "Jet fuel":    analytics.gallons_to_barrel(prices["jet_fuel"]),
    "Diesel-jet spread": diesel_jet_spread(prices),
    "Diesel-jet z-score": diesel_jet_spread_zscore(prices),
})

# Sidebar date filter
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Date range",
    value=(config.START_DATE, in_bbl.index.max().date()),
)

if len(date_range) != 2:        # user is mid-selection — wait for both dates
    st.stop()
start, end = date_range
view = in_bbl[(in_bbl.index.date >= start) & (in_bbl.index.date <= end)]

st.subheader("Prices Crude ($/bbl)")
st.line_chart(view[["Brent crude"]])

crack = analytics.crack_spread(in_bbl["Heating oil"], in_bbl["Brent crude"])
st.subheader("Distillate heating oil/crude crack ($/bbl)")
st.line_chart(crack[(crack.index.date >= start) & (crack.index.date <= end)])

st.subheader("Diesel-jet spread ($/bbl)")
st.line_chart(view["Diesel-jet spread"])

st.subheader("Diesel-jet spread z-score")
st.line_chart(view["Diesel-jet z-score"])


characteristic = cv.classify_snapshot(curve)

st.subheader(f"Heating oil term structure (next {n_months} contracts): {characteristic}")
chart = (
    alt.Chart(curve)
    .mark_line(point=True)
    .encode(
        x=alt.X("contract:N", sort=list(curve["contract"]), title="Contract"),
        y=alt.Y("price:Q", title="Price"),
        tooltip=["contract", "price", "month_offset"],
    )
)
st.altair_chart(chart, use_container_width=True)