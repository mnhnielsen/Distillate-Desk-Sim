# DistillateDesk

A mini "trading desk" for middle distillates — built to show I can **code like an
engineer and think like an energy trader**. It ingests crude and distillate prices,
builds crack spreads, and (over the coming phases) backtests a strategy and runs a
fuel-hedging simulator.

> Full build plan and rationale: see `distillate-desk-project-spec.md`.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m src.ingest    # pull Brent + distillate prices -> data/prices.parquet
python -m src.plot      # write crack_overview.png
pytest                  # run the analytics tests
```

## What's here (Phase 0–1)

| File | Does |
|---|---|
| `src/config.py` | Tickers, units (42 gal/bbl), date range, paths |
| `src/ingest.py` | Download daily prices from Yahoo Finance, store as parquet |
| `src/analytics.py` | Pure functions: gallons→barrel, crack spread, rolling z-score |
| `src/plot.py` | Quick crude-vs-distillate + crack-spread chart |
| `tests/` | Unit tests for the analytics |

## Data note

`HO=F` (NY Harbor ULSD / heating oil) is an accessible **distillate proxy**, quoted in
USD/gallon — converted to USD/barrel before computing the crack. In a production setting
I'd swap in **ICE Gasoil** (the European benchmark) or Platts/Argus assessments.

## Roadmap

- **Phase 1** — diesel–jet spread, forward-curve / contango vs backwardation, a Streamlit dashboard
- **Phase 2** — backtest engine for a mean-reversion crack strategy (with costs, honest evaluation)
- **Phase 3** — Monte-Carlo fuel-hedging simulator + position-keeping & VaR
- **Phase 4** — biofuel/FuelEU blend economics, or option pricing (Black-76)
