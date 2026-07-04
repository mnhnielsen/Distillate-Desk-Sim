"""Pull historical prices from Yahoo Finance and store them locally.

Run from the repo root:  python -m src.ingest
"""
from __future__ import annotations
import time

import pandas as pd
import yfinance as yf
from . import eia_data as eia
from . import config


def _close_series_yf(raw: pd.DataFrame) -> pd.Series:
    """Extract a 1-D close-price series across yfinance versions."""
    close = raw["Close"]
    if isinstance(close, pd.DataFrame):   # newer yfinance returns a frame
        close = close.iloc[:, 0]
    return close

def _close_series(raw: pd.DataFrame) -> pd.Series:
    close = None
    if isinstance(raw, pd.DataFrame):
        close = raw.iloc[:, 0]
    return close


def fetch_prices(tickers: dict[str, str], start: str) -> pd.DataFrame:
    """Download daily close prices; return one column per instrument."""
    print(f"Fetching prices from {config.START_DATE} to today...")
    frames = {}
    for name, ticker in tickers.items():
        raw = yf.download(ticker, start=start, progress=False, interval='5D', auto_adjust=False)
        if raw.empty:
            raw = eia.get_distillate_spot_prices(id=ticker, start_date=start, end_date=None, frequency='monthly')
            if raw.empty:
                 raise RuntimeError(f"No data returned for {ticker} ({name}).")
            frames[name]=_close_series(raw)
            continue
        frames[name] = _close_series_yf(raw)
    prices = pd.concat(frames, axis=1)
    prices.columns = list(tickers.keys())
    return prices.dropna(how="all").ffill()


def main() -> None:
    prices = fetch_prices(config.TICKERS, config.START_DATE)
    prices.to_parquet(config.PRICES_FILE)
    print(f"Saved {len(prices):,} rows to {config.PRICES_FILE}")
    print(prices.tail())


if __name__ == "__main__":
    main()
