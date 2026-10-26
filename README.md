# The Attention Lab

An interactive, compact Instagram audience and content analytics portfolio dashboard, built with **Python**, **pandas**, **Plotly**, **Streamlit**, and **SQLite/SQL**.

## Live dashboard
Add your Streamlit URL here after deploying.

## What it analyzes
- Instagram account-level content views, reach, and engaged accounts
- Follower trajectory and day-by-day net follower changes
- Reel-level likes and comments, publishing cadence
- Follower demographics at the data retrieval date
- Data availability and a proposed (not conducted) experiment

## Run locally
```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

## SQL analysis
```bash
python3 build_database.py
sqlite3 attention_lab.sqlite < analysis.sql
```

## Data and methodological limits
Muse-exported analytics cover approximately July 25 to October 25, 2026. Reel-level data includes likes and comments, but not per-Reel views, reach, saves, shares, watch time, or follows. Account-level totals are **not** interchangeable with post-level metrics. Post interactions were retrieved later than their publication, so daily post-level likes are not likes earned on the publication day. The dashboard does not claim player retention, content causality, or a completed A/B test.

## Data privacy
The `data/` directory contains real public-portfolio Instagram account analytics, including post URLs, captions, follower counts, and aggregate audience-demographic breakdowns. Review before publishing the repo.

## Portfolio context
The project illustrates behavioural analytics methods transferable to product analytics, but it is not gameplay telemetry. SQL queries demonstrate JOINs, aggregations, CTEs, and window functions.
