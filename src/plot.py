"""Quick visual sanity check of the stored price data.

Run from the repo root:  python -m src.plot
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from . import analytics, config


def load_prices() -> pd.DataFrame:
    return pd.read_parquet(config.PRICES_FILE)

def diesel_jet_spread_zscore(prices: pd.DataFrame) -> pd.Series:
    dieselbbl = analytics.gallons_to_barrel(prices["diesel_jet"])
    jetbbl = analytics.gallons_to_barrel(prices["jet_fuel"])
    
    diesel_jet_spread = analytics.diesel_jet_spread(dieselbbl, jetbbl)
    diesel_jet_zscore = analytics.zscore(diesel_jet_spread)
    return diesel_jet_zscore

def diesel_jet_spread_spread(prices: pd.DataFrame) -> pd.Series:
    dieselbbl = analytics.gallons_to_barrel(prices["diesel_jet"])
    jetbbl = analytics.gallons_to_barrel(prices["jet_fuel"])
    
    diesel_jet_spread = analytics.diesel_jet_spread(dieselbbl, jetbbl)
    return diesel_jet_spread


def main() -> None:
    prices = load_prices()
    distillate_bbl = analytics.gallons_to_barrel(prices["heating_oil"])
    crack = analytics.crack_spread(distillate_bbl, prices["brent"])
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    ax1.plot(prices.index, prices["brent"], label="Brent crude ($/bbl)")
    ax1.plot(prices.index, distillate_bbl, label="Distillate ($/bbl)")
    ax1.set_title("Crude vs distillate")
    ax1.legend(); ax1.grid(alpha=0.3)

    ax2.plot(crack.index, crack, color="tab:green", label="Distillate crack ($/bbl)")
    ax2.axhline(0, color="grey", lw=0.8)
    ax2.set_title("Distillate crack spread")
    ax2.legend(); ax2.grid(alpha=0.3)

    fig.tight_layout()
    out = config.ROOT / "crack_overview.png"
    fig.savefig(out, dpi=120)
    print(f"Chart saved to {out}")


if __name__ == "__main__":
    main()
