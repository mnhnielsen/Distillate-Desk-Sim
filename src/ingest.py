"""Pull historical prices from Yahoo Finance and store them locally.

Run from the repo root:  python -m src.ingest
"""
from __future__ import annotations

import pandas as pd
import yfinance as yf
import eia_data as eia
import config


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


def fetch_prices(tickers: dict[str, tuple[str, str]], start: str) -> pd.DataFrame:
    """Download daily close prices; return one column per instrument.

    Each ticker entry is a (source, symbol) pair — "yahoo" or "eia" — so a
    bad or empty response from one source fails loudly instead of silently
    being retried against the other.
    """
    print(f"Fetching prices from {start} to today...")
    frames = {}
    for name, (source, ticker) in tickers.items():
        if source == "yahoo":
            raw = yf.download(ticker, start=start, progress=False, interval='1D', auto_adjust=False)
            if raw.empty:
                raise RuntimeError(f"No data returned for {ticker} ({name}).")
            frames[name] = _close_series_yf(raw)
        elif source == "eia":
            raw = eia.get_distillate_spot_prices(id=ticker, start_date=start, end_date=None, frequency='daily')
            if raw.empty:
                raise RuntimeError(f"No data returned for {ticker} ({name}).")
            frames[name] = _close_series(raw)
        else:
            raise ValueError(f"Unknown data source {source!r} for {name}.")
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
