"""Central configuration for DistillateDesk."""
from pathlib import Path

# --- Paths ---
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
PRICES_FILE = DATA_DIR / "prices.parquet"

# --- Instruments (Yahoo Finance tickers) ---
# Brent is the crude benchmark; HO=F (NY Harbor ULSD / heating oil) is an
# accessible middle-distillate proxy. Swap in ICE Gasoil / Platts data later.
CRUDE_TICKER = "BZ=F"        # Brent crude  -> quoted in USD/BARREL
DISTILLATE_TICKER = "HO=F"   # ULSD         -> quoted in USD/GALLON
TICKERS = {
    "brent": CRUDE_TICKER,
    "heating_oil": DISTILLATE_TICKER,
}

# --- Conventions ---
GALLONS_PER_BARREL = 42      # 1 US barrel = 42 US gallons

# --- History ---
START_DATE = "2021-01-01"
