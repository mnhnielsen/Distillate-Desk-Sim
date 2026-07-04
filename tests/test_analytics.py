"""Unit tests for the core analytics. Run: pytest"""
import pandas as pd

from src import analytics


def test_gallons_to_barrel():
    s = pd.Series([1.0, 2.0])
    out = analytics.gallons_to_barrel(s, gallons_per_barrel=42)
    assert list(out) == [42.0, 84.0]


def test_crack_spread():
    product = pd.Series([95.0, 100.0])   # $/bbl
    crude = pd.Series([80.0, 82.0])      # $/bbl
    out = analytics.crack_spread(product, crude)
    assert list(out) == [15.0, 18.0]


def test_zscore_rising_series_is_positive():
    s = pd.Series(range(100), dtype=float)   # steadily rising
    z = analytics.zscore(s, window=10)
    assert z.iloc[-1] > 0
