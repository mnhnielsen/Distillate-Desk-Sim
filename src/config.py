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
JETFUEL_TICKER = "EER_EPJK_PF4_RGC_DPG"        # Jet fuel, US Gulf Coast   -> USD/GALLON
DIESEL_TICKER = "EER_EPD2DXL0_PF4_RGC_DPG"     # ULSD diesel, US Gulf Coast -> USD/GALLON
DIESEL_NYH_TICKER = "EER_EPD2DXL0_PF4_Y35NY_DPG"  # ULSD diesel, NY Harbor -> USD/GALLON

# Diesel and jet are both US Gulf Coast so the diesel-jet spread is a clean
# product spread; the NY Harbor diesel series is kept so the NYH-USGC
# *location* spread can be studied separately.
# Each instrument declares its data source, so ingest dispatches explicitly
# instead of trying Yahoo first and falling back on an empty response.
TICKERS = {
    "brent":       ("yahoo", CRUDE_TICKER),
    "heating_oil": ("yahoo", DISTILLATE_TICKER),
    "diesel":      ("eia", DIESEL_TICKER),
    "diesel_nyh":  ("eia", DIESEL_NYH_TICKER),
    "jet_fuel":    ("eia", JETFUEL_TICKER),
}


# --- Conventions ---
GALLONS_PER_BARREL = 42      # 1 US barrel = 42 US gallons

# --- History ---
START_DATE = "2010-12-01"
