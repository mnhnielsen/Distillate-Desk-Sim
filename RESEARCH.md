# Research notes

Dated observations from the data, honest caveats included. Numbers regenerate from
`data/prices.parquet`; charts referenced here are `diesel_jet_overview.png` and
`crack_overview.png`.

## Definitions

- **Diesel–jet spread** = USGC ULSD − USGC jet, both converted to $/bbl (×42 from EIA's $/gal).
  Both legs are US Gulf Coast, so this is a clean *product* spread.
- **Location spread** = NY Harbor ULSD − USGC ULSD, $/bbl. Isolates the *regional* component.
- **Distillate crack** = HO front-month ($/bbl) − Brent front-month ($/bbl). A simple 1:1 crack,
  not a 3-2-1 refinery yield.
- **Z-score** = 60-trading-day rolling z of the spread (~3 calendar months).

---

## 2026-07-21 — The April–May diesel–jet inversion was deeper than first measured

The USGC diesel–jet spread went negative on **2026-04-10** and bottomed at
**−11.55 $/bbl on 2026-05-18** (z-score trough −2.46 on 2026-04-16). Jet trading *over*
diesel by double digits is a rare configuration — normally diesel carries a premium.

My first measurement of this episode used NY Harbor diesel against Gulf Coast jet. That
cross-regional version only fell to −3.36 $/bbl, because the NYH diesel premium over USGC
(~4.5 $/bbl average through 2025) was *masking* the depth of the product move. Redefining
the spread with both legs on the Gulf Coast revealed the inversion was roughly 3× larger
than the mixed measure suggested.

**Lesson:** always separate product basis from locational basis before interpreting a spread.

- [ ] TODO: find the fundamental driver of the inversion (jet demand spike? diesel imports?)
      and note it here.

## 2026-07-21 — The diesel location spread is itself a signal

NYH−USGC diesel averaged ~2.5 $/bbl in 2024, ~4.5 $/bbl in 2025, spiked to **10.79 $/bbl
on 2026-03-12**, and briefly went *negative* in April 2026 — i.e. Gulf Coast barrels
commanded a premium over New York, which is unusual given the normal south-to-north flow
(Colonial pipeline economics). The location spread is volatile enough that any "diesel"
signal built on a single region inherits it silently.

## 2026-07-21 — Distillate crack at the 99.6th percentile; curve backwardated

The HO–Brent crack printed **~78 $/bbl** (2026-07-21), against a full-history median of
17 $/bbl. It is at the **99.6th percentile** of all history since 2013. Only two years
have ever printed above 60 $/bbl: 2022 (56 days, post-Ukraine squeeze, peak 108) and 2026
(55 days so far, 2026 high 85.1 on 2026-07-16). The HO futures curve is simultaneously in
**backwardation** (front over back — prompt barrels bid), consistent with near-term
physical tightness rather than a term repricing.

Together the picture reads like a 2022-style distillate squeeze: extreme flat-price crack,
prompt premium, and a diesel–jet spread that snapped back violently from the May inversion
to +16.8 $/bbl (z ≈ +0.9) now.

- [ ] TODO: track whether the crack mean-reverts or plateaus (2022 stayed elevated for
      months — mean reversion assumptions failed there).

---

## Caveats (read before trusting any number above)

1. **EIA publication lag.** The last true EIA print is 2026-07-13; later spread rows are
   forward-filled, so the newest spread/z values are stale by up to a week. Yahoo legs
   (Brent, HO) are current.
2. **Spot assessments are not tradable.** EIA series are daily spot assessments. The
   tradable expressions are HO/gasoil futures or swaps; realized P&L would differ by basis
   and roll. Any backtest on these series is a *signal* study, not a P&L study.
3. **No seasonality adjustment.** Heating oil demand is winter-weighted, jet is
   summer-weighted; the diesel–jet spread has a seasonal shape that the 60-day z-score
   only partially absorbs. A seasonal (e.g. same-month historical) benchmark would be cleaner.
4. **Crack history starts ~2013** — Yahoo's Brent futures history is shorter than the EIA
   series, so percentile claims cover 2013→today (~3,950 obs).
