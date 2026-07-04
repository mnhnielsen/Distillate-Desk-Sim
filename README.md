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

Symbols from EIA:

`JETFUEL = "EER_EPJK_PF4_RGC_DPG"`

`DIESEL = "EER_EPD2DXL0_PF4_Y35NY_DPG"`

## Roadmap

- **Phase 1** — diesel–jet spread, forward-curve / contango vs backwardation, a Streamlit dashboard
- **Phase 2** — backtest engine for a mean-reversion crack strategy (with costs, honest evaluation)
- **Phase 3** — Monte-Carlo fuel-hedging simulator + position-keeping & VaR
- **Phase 4** — biofuel/FuelEU blend economics, or option pricing (Black-76)

## Observations

- In late April 2026 the diesel-jet spread narrowed a lot and go inverse, collapsing from spreads 0.25 to -0.051 in start May. I also tracked the z score to collapse to a -4
- As of this run (July 26), the market reading from my function is that heating oil curve based on the future prices is in backwardation, meaning the markets paying a premium for promt barrels over deffered barrels, meaning a near-term tightness.
