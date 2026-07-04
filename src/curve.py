from __future__ import annotations
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import analytics, config

_MONTH_CODES = "FGHJKMNQUVXZ"

def _close_series_yf(raw: pd.DataFrame) -> pd.Series:
    close = raw["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return close

def contract_symbol(root: str, month: int, year: int) -> str:
    """root='HO', month=8, year=2026 -> 'HOQ26.NYM'."""
    return f"{root}{_MONTH_CODES[month - 1]}{year % 100:02d}.NYM"

def fetch_contract(root: str, month: int, year: int, period: str = "1y") -> pd.Series:
    """Daily close history for ONE contract."""
    sym = contract_symbol(root, month, year)
    raw = yf.download(sym, period=period, progress=False, auto_adjust=False)
    if raw.empty:
        raise RuntimeError(f"No data for {sym}")
    return _close_series_yf(raw).dropna()

def _next_month(today: dt.date | None = None) -> dt.date:
    """First day of next month — skips the current, expiring front contract."""
    today = today or dt.date.today()
    year = today.year + (today.month // 12)
    month = today.month % 12 + 1
    return dt.date(year, month, 1)

def curve_snapshot(root: str, months: int, start: dt.date | None = None) -> pd.DataFrame:
    """Latest close for each of the next `months` contracts -> today's curve."""
    start = start or _next_month()
    rows, y, m = [], start.year, start.month
    for offset in range(months):
        try:
            price = float(fetch_contract(root, m, y, period="1mo").iloc[-1])
            rows.append({"contract": contract_symbol(root, m, y),
                         "month_offset": offset, "price": price})
        except Exception:
            pass
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return pd.DataFrame(rows)

def classify_snapshot(curve: pd.DataFrame) -> str:
    """Label the whole curve from its front (first) vs back (last) contract."""
    if len(curve) < 2:
        return "flat"
    return analytics.classify_term_structure(curve["price"].iloc[0],
                                             curve["price"].iloc[-1])

def spread_over_time(root: str, front: tuple[int, int], back: tuple[int, int]) -> pd.Series:
    """front - back per day, over history (for z-scoring)."""
    front_s = fetch_contract(root, *front, period="1y")
    back_s  = fetch_contract(root, *back,  period="1y")
    return analytics.term_structure(front_s, back_s).dropna()

def plot_curve(curve: pd.DataFrame) -> None:
    shape = classify_snapshot(curve)
    plt.figure(figsize=(8, 5))
    plt.plot(curve["month_offset"], curve["price"], marker="o")
    plt.xticks(curve["month_offset"], curve["contract"], rotation=45, ha="right")
    plt.title(f"HO forward curve — {shape}")
    plt.ylabel("$/gallon"); plt.grid(alpha=0.3); plt.tight_layout()
    out = config.ROOT / "curve.png"
    plt.savefig(out, dpi=120)
    print(f"Saved {out}")
    
    

# curve = curve_snapshot("HO", months=7)
# print(curve)
# print("Shape:", classify_snapshot(curve))
# plot_curve(curve)