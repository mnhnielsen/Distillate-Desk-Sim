# DistillateDesk

A mini "trading desk" for middle distillates. It ingests crude and middle distillate prices, such as Diesel and Jetfuel
builds crack spreads, and (over the coming phases) backtests a strategy and runs a
fuel-hedging simulator.

Full build plan and rationale: see `distillate-desk-project-spec.md`.

## Data note

`HO=F` (NY Harbor ULSD / heating oil) is an accessible **distillate proxy**, quoted in
USD/gallon — converted to USD/barrel before computing the crack. In a production setting
I'd swap in **ICE Gasoil** (the European benchmark) or Platts/Argus assessments.

Data are mainly from Yahoo Finance for Heating Oil and general oil prices but they don't carry prices for distillates. These prices come from EIA.

Symbols from EIA (diesel and jet are both **US Gulf Coast**, so the diesel–jet spread is a
clean product spread; NY Harbor diesel is kept separately to study the location spread):

`JETFUEL = "EER_EPJK_PF4_RGC_DPG"` — jet fuel, US Gulf Coast

`DIESEL = "EER_EPD2DXL0_PF4_RGC_DPG"` — ULSD, US Gulf Coast

`DIESEL_NYH = "EER_EPD2DXL0_PF4_Y35NY_DPG"` — ULSD, NY Harbor

## Roadmap

- **Phase 1** — diesel–jet spread, forward-curve / contango vs backwardation, a Streamlit dashboard
- **Phase 2** — backtest engine for a mean-reversion crack strategy (with costs, honest evaluation)
- **Phase 3** — Monte-Carlo fuel-hedging simulator + position-keeping & VaR
- **Phase 4** — biofuel/FuelEU blend economics, or option pricing (Black-76)

## Observations

Dated research notes live in [RESEARCH.md](RESEARCH.md). Headlines so far:

- The April–May 2026 diesel–jet inversion bottomed at **−11.55 $/bbl** — and was ~3× deeper
  than my first (cross-regional) measurement showed, a lesson in separating product basis
  from locational basis.
- The distillate crack is at the **99.6th percentile** of its history with the HO curve in
  backwardation — the market is paying a premium for prompt barrels over deferred, a
  2022-style near-term tightness.
