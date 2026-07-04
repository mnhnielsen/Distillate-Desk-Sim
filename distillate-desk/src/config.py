"""Central configuration for DistillateDesk."""
from pathlib import Path

# --- Paths ---
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
PRICES_FILE = DATA_DIR / "prices.parquet"

# --- Instruments (YF Tickers and EIA Ids) ---
# Brent is the crude benchmark; HO=F (NY Harbor ULSD / heating oil) is an
# accessible middle-distillate proxy. Swap in ICE Gasoil / Platts data later.
CRUDE_TICKER = "BZ=F"        # Brent crude  -> quoted in USD/BARREL
DISTILLATE_TICKER = "HO=F"   # ULSD         -> quoted in USD/GALLON
JETFUEL_TICKER = "EER_EPJK_PF4_RGC_DPG"      # Jet fuel     -> quoted in USD/GALLON
DIESEL_TICKER = "EER_EPD2DXL0_PF4_Y35NY_DPG"   # Diesel       -> quoted in USD/GALLON
TICKERS = {
    "brent": CRUDE_TICKER,
    "heating_oil": DISTILLATE_TICKER,
    "diesel_jet": DIESEL_TICKER,
    "jet_fuel": JETFUEL_TICKER
}


# --- Conventions ---
GALLONS_PER_BARREL = 42      # 1 US barrel = 42 US gallons

# --- History ---
START_DATE = "2025-12-01"
