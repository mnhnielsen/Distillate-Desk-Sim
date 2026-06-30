# DistillateDesk — Portfolio Project Spec

**A mini "trading desk" for middle distillates.** One project that proves you can *code like an engineer and think like an energy trader* — built around oil, diesel, jet and the crack spread.

This is the single strongest signal you can send to a commodity-trading desk: it touches every line of the GRM-style job description (price-curve management, position keeping, trade valuation, research, proprietary strategy development) and it grows naturally out of your existing Python fuel-bidding-auction project and your Bunker Holding background.

---

## Why this project works

- **It's commercial, not just technical.** Most dev portfolios show CRUD apps. This shows market thinking.
- **It mirrors GRM's actual business** — pricing, hedging, position keeping — so you can talk about it fluently in an energy-trading interview.
- **It's modular**, so you have something impressive to show after one weekend, and something deep after a few weeks.
- **It plays to your edge**: you've seen the *physical* fuel side at Bunker Holding; this models the *paper* side that trades around it.

> **The one-line pitch for your CV / interview:**
> "I built a middle-distillates analytics and hedging toolkit in Python — it ingests crude, diesel and jet prices, builds forward curves and crack spreads, backtests a mean-reversion strategy, and runs a Monte-Carlo hedging simulator for a shipping client's fuel exposure."

---

## Tech stack

| Layer | Tools |
|---|---|
| Language | Python 3.11+ |
| Data / analysis | pandas, numpy, statsmodels, scikit-learn |
| Charts | plotly (interactive) or matplotlib |
| Dashboard | Streamlit (fastest path to a shareable UI) |
| Storage | DuckDB or SQLite + parquet files |
| Ingestion | requests; the EIA / FRED APIs; `yfinance`; Stooq |
| Engineering polish | pytest, type hints, GitHub Actions (scheduled data refresh), a clean README |

Keep it a clean, documented repo. **Repo hygiene is itself part of the signal** — traders trust people whose code looks careful, because careless code is how books blow up.

---

## Free data sources

- **EIA** (`eia.gov`, free API key): crude, No.2 distillate (diesel), jet fuel, heating oil — clean and reliable.
- **FRED** (St. Louis Fed, free API): WTI/Brent spot and product prices.
- **`yfinance`**: futures — `BZ=F` (Brent), `CL=F` (WTI), `HO=F` (NY Harbor ULSD — a good **diesel/distillate proxy**), `RB=F` (gasoline).
- **Stooq**: free historical futures CSVs.

> Note: the European distillate benchmark is **ICE Gasoil (low-sulphur gasoil)**. Free history for it is harder to get, so use **heating oil `HO=F` as your distillate proxy** and mention in your README that you'd swap in ICE Gasoil / Platts / Argus data in a production setting. Saying that out loud shows you know the *real* benchmarks.

---

## Architecture — six modules

1. **Data layer** — ingestion + storage + a refresh pipeline. Pull crude, diesel/heating-oil, jet, gasoline into a tidy local store.
2. **Curve module** — build a forward curve from the futures strip; detect and visualise **contango vs backwardation**; track how the curve shape changes over time.
3. **Analytics module** — compute **crack spreads** (distillate crack vs crude; a 3:2:1 proxy), the **diesel–jet spread**, rolling stats, seasonality, and **z-scores** to flag when a spread looks rich or cheap.
4. **Backtest engine** — implement and honestly evaluate one well-reasoned strategy (e.g. mean-reversion on the crack z-score). Include **transaction costs**, P&L, Sharpe, max drawdown.
5. **Hedging simulator** — the "GRM business" module. Model a shipping client with monthly fuel needs; simulate hedging with swaps; **Monte-Carlo** the price paths and compare the **hedged vs unhedged P&L distribution**.
6. **Risk + dashboard** — toy **position-keeping** book with **mark-to-market** and a simple **VaR**; tie everything together in a **Streamlit** app.

---

## Phased roadmap

Ship each phase as a working, documented increment. You want a presentable result *early*.

### Phase 0 — Foundations *(a weekend)*
- Repo, README, virtual env, project structure.
- Ingest crude (`BZ=F`) + distillate (`HO=F`); store locally; plot price history.
- **Deliverable:** a repo that pulls and charts real energy prices. Already shareable.

### Phase 1 — Cracks & curves *(~1 week)*
- Crack-spread calculation + the diesel–jet spread.
- Forward-curve construction; contango/backwardation visual.
- A first **Streamlit dashboard**: pick a date range, see prices, cracks, curve shape.
- **Deliverable:** an interactive distillates dashboard. *This alone is a strong portfolio piece.*

### Phase 2 — Research & backtest *(~1–2 weeks)*
- Z-score signal on the crack; a mean-reversion strategy.
- Backtest engine with costs; P&L, Sharpe, drawdown; equity curve.
- A short **`RESEARCH.md`** writing up the idea, results, **and the honest caveats** (see below).
- **Deliverable:** a backtested strategy with a credible, self-critical write-up.

### Phase 3 — Hedging & risk *(~1–2 weeks)*
- Monte-Carlo price-path simulator; the shipping-client hedging case; hedged-vs-unhedged distributions.
- Position-keeping book + mark-to-market + VaR.
- **Deliverable:** the module that maps directly onto GRM's actual hedging business.

### Phase 4 — Stretch *(pick one)*
- **Biofuel / FuelEU angle:** model B30 blend economics and a FuelEU compliance-cost estimate. Ties straight to GRM's green-fuels focus and makes you stand out.
- **Options:** price a simple hedging option with **Black-76** on futures; add it to the hedging simulator.
- **Live ops:** a scheduled GitHub Action that refreshes data daily and updates the dashboard — shows production-engineering maturity.

---

## Be honest about the backtest (this is a feature, not a weakness)

Trading desks are deeply sceptical of backtests, so **demonstrating that scepticism yourself is a green flag.** In your write-up, explicitly address:

- **Look-ahead bias** — only use information available at the time of each signal.
- **Transaction costs & slippage** — a strategy that only works at zero cost works nowhere.
- **Overfitting** — don't tune endlessly to make a pretty curve; report what *didn't* work too.
- **Regime dependence** — note that a 2022–2026 backtest spans wild events (war, sanctions); results may not generalise.

A modest, honestly-evaluated strategy beats a spectacular one you clearly curve-fit. Saying *"here's why I don't fully trust this result"* is exactly how a good trader talks.

---

## How to present it in interviews

Map each module to the job, out loud:

- *"Real-time price-curve management"* → your curve module.
- *"Diligent and accurate position keeping"* → your risk book + mark-to-market.
- *"Trade valuation"* → mark-to-market + the hedging simulator.
- *"Research and market analysis"* → the crack-spread analytics + your `RESEARCH.md`.
- *"Development of new proprietary trading strategies"* → the backtest engine.

Then close the loop on your story: *"I saw the physical fuel side at Bunker Holding; I built this to understand and model the paper side that trades around it."*

**Repo checklist before you share it:** clear README with screenshots, a one-command run, tests on the core calculations, no secrets committed, and a short `RESEARCH.md`. A recruiter or trader should grasp what it does in 30 seconds and be able to run it in two minutes.

---

## Thesis tie-in

This project is also a natural **thesis springboard**. "Forecasting middle-distillate crack spreads" or "Backtesting hedging strategies for marine fuel exposure" — ideally in collaboration with an energy-trading firm — turns this portfolio piece into an academic credential *and* a foot in the door at the same time.
