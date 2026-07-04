# DistillateDesk — Build Checklist

A step-by-step to-do list for taking the project from a running starter to a portfolio piece.
Work top to bottom, commit after each step, and build **one tested function at a time**.

---

## Phase 0 — Foundations

- [ ] **Set up the environment** — `python -m venv .venv && source .venv/bin/activate`, then `pip install -r requirements.txt`.
- [ ] **Pull the data** — run `python -m src.ingest`; it saves Brent + heating-oil prices to `data/prices.parquet` (needs internet).
- [ ] **Eyeball it** — run `python -m src.plot` and check `crack_overview.png` looks sane: a crude line, a distillate line, and a crack spread.
- [ ] **Confirm the logic** — run `pytest`; all tests should pass before you build anything new.
- [ ] **Put it on GitHub** — `git init`, commit, push to a *public* repo; this is what you'll share.
- [ ] **Read every line in `src/`** — you must be able to explain each one in an interview.
- [ ] **Get an EIA API key** — free at eia.gov/opendata; you'll need it in Phase 1.

---

## Phase 1 — Cracks, spreads & a dashboard

**Diesel–jet spread (easy win — start here)**
- [ ] **Add `diesel_jet_spread()`** to `analytics.py` — it's the same shape as `crack_spread`: just subtract jet from diesel (both in $/bbl).
- [ ] **Test it** — mirror `test_crack_spread`; keep `pytest` green.

**Get jet + diesel data (Yahoo has no jet)**
- [ ] **Write `src/eia.py`** — pull daily spot prices from the EIA v2 API with `requests`, save to `data/eia_prices.parquet`; mirror the structure of `ingest.py`.
- [ ] **Find + verify the series IDs** — NY Harbor ULSD (diesel) and Gulf Coast jet fuel; confirm them in the EIA browser, because the IDs are the brittle part, not the code.
- [ ] **Mind the units** — EIA products are quoted in **$/gallon**, so reuse `gallons_to_barrel` before computing any spread.

**Signal + sanity check**
- [ ] **Run `zscore` on the diesel–jet spread** — confirm the spikes line up with the early-2026 distillate surge; absurd numbers almost always mean a unit bug, so check the gallon→barrel step first.

**Term structure (front vs back month)**
- [ ] **Add `term_structure()` and `classify_curve()`** to `analytics.py` — research **contango** (later months dearer) vs **backwardation** (front dearer) so your labels are right; test `classify_curve`.
- [ ] **Attempt a curve pull in `src/curve.py`** — best-effort via Yahoo contract symbols (root + month code + 2-digit year + `.NYM`); keep whatever returns data and note in the README that free curve data is flaky. **Treat this as a bonus, not a blocker.**

**Dashboard**
- [ ] **Build `src/dashboard.py` in passes** — first load the parquet files and draw prices, then add crack → diesel–jet → z-score → curve, one panel at a time.
- [ ] **Research the Streamlit basics you need** — `st.line_chart`, `st.sidebar`, `st.date_input`, `@st.cache_data`; run it with `streamlit run src/dashboard.py`.
- [ ] **Make every panel defensive** — if a data file is missing, show a message instead of crashing; that robustness is itself a signal.

**Wrap up**
- [ ] **Start `RESEARCH.md`** — write 3–4 honest observations from the data and commit each step as you go.

---

## Phase 2 — Research & backtest

- [ ] **Define a signal** — e.g. go long the crack when its z-score drops below −1 and exit when it returns to 0 (mean reversion).
- [ ] **Write a backtest engine** — turn the signal into daily positions, compute P&L as position × price change, and subtract transaction costs.
- [ ] **Kill look-ahead bias** — shift signals by one day so you only ever trade on information you'd actually have had.
- [ ] **Compute the metrics** — cumulative P&L, Sharpe ratio, max drawdown; plot the equity curve.
- [ ] **Test the engine** — run it on a tiny synthetic price series where you can work out the answer by hand.
- [ ] **Write it up honestly in `RESEARCH.md`** — address costs, overfitting and regime dependence, and report what *didn't* work; self-critical beats spectacular.

---

## Phase 3 — Hedging simulator & risk

- [ ] **Simulate price paths** — generate many possible futures with geometric Brownian motion (research: drift, volatility, `numpy` random); this is the heart of the simulator.
- [ ] **Model a shipping client** — a fixed monthly fuel volume; compare unhedged cost vs swap-hedged cost across all simulated paths and plot the two P&L distributions side by side.
- [ ] **Add position keeping** — a small book of trades you mark-to-market against the latest price.
- [ ] **Add a simple VaR** — historical or parametric 95% on the book; research what VaR means *and* its limitations, and say so.

---

## Phase 4 — Stretch *(pick one)*

- [ ] **Biofuel / FuelEU angle** — model a B30 blend cost and a rough FuelEU compliance-cost estimate; this ties straight to GRM's green-fuels focus and makes you stand out.
- [ ] **Option pricing** — price a hedging option with Black-76 on futures and fold it into the hedging sim (research: Black-76 and the Greeks).
- [ ] **Live ops** — a scheduled GitHub Action that refreshes the data daily; shows production-engineering maturity.

---

## Before you show it off

- [ ] **README sells it in 30 seconds** — what it does, a screenshot, and a one-command run.
- [ ] **Tests cover the core calculations** — and no secrets are committed (`.gitignore` your API key).
- [ ] **Rehearse the mapping out loud** — tie each module to a job-ad line: price-curve management, position keeping, trade valuation, research, proprietary strategy development.

---

### Working principles

- **One tested function at a time** — the Phase 0 files are your template for everything that follows.
- **Headline feature first** — the diesel–jet spread via EIA is the reliable, valuable core; don't let the fragile curve data stall you.
- **Commit small and often** — a steady GitHub history reads exactly like good desk discipline.