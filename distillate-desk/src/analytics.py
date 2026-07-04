"""Core market analytics: unit conversion, cracks, spreads and signals.

These are pure functions (data in, data out) so they're trivial to test and
reusable across the dashboard, backtest and hedging modules to come.
"""
from __future__ import annotations

import pandas as pd

import config


def gallons_to_barrel(price_per_gallon: pd.Series, gallons_per_barrel: int = config.GALLONS_PER_BARREL) -> pd.Series:
    """Convert a USD/gallon price series to USD/barrel."""
    return price_per_gallon * gallons_per_barrel


def crack_spread(product_per_bbl: pd.Series, crude_per_bbl: pd.Series) -> pd.Series:
    """Refining-margin proxy: product price minus crude price, both USD/bbl."""
    return product_per_bbl - crude_per_bbl

def diesel_jet_spread(diesel_per_bbl: pd.Series, jet_per_bbl: pd.Series) -> pd.Series:
    """Diesel minus jet, both in USD/bbl."""
    return diesel_per_bbl - jet_per_bbl

def zscore(series: pd.Series, window: int = 60) -> pd.Series:
    """Rolling z-score: standard deviations from the rolling mean.

    A high positive z means the spread looks rich vs its recent history;
    a low negative z means it looks cheap -- the basis of a mean-reversion idea.
    """
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std

def term_structure(front, back) -> float:
    """Return the difference between two contract prices, e.g. front minus back."""
    return front - back

def classify_term_structure(front, back) -> str:
    diff = term_structure(front, back)
    if diff > 0:
        return "backwardation"
    elif diff < 0:
        return "contango"
    return "flat"
