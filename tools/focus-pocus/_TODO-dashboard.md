# TODO — revisit the Focus Pocus stats dashboard

**Delete this file (and `_make_dashboard.py`) once done.** The `_` prefix keeps both out of the
Quarto build, so they won't appear on the site.

## What's here
`stats-dashboard.png` was regenerated with a consistent color rule:

> **Navy = objective data the app measured. Gold = my own self-rating.**

(Previously gold was doing three different jobs — peak-day bar, a data series, and a mean line —
which read as inconsistent. Now gold means *only* "my self-assessment.")

## ⚠️ Why to revisit
The data in the current figure was **transcribed by eye from the OLD png** — it is approximate,
not the real export. The caption calls these "my own real sessions," so the numbers should be true.

## To finish
1. Export the real session data from the Focus Pocus app (CSV/JSON).
2. Open `_make_dashboard.py`, replace the hand-typed arrays (`hours`, `measured`, `selfeff`,
   `wk_counts`) with the real values.
3. Regenerate:
   `& "C:\Users\User\anaconda3\python.exe" _make_dashboard.py`
   (or whatever your Python is on the new machine — needs `matplotlib` + `numpy`).
4. Check the PNG, then delete this note and `_make_dashboard.py`.

## Also still open
- Confirm the privacy claims in `index.qmd` ("Your data never leaves your machine") are exactly
  accurate for the shipped app.
