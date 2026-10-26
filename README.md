# @linsvideodiary | Instagram Insights

An interactive, compact Instagram audience and content analytics portfolio dashboard, built with **Python**, **pandas**, **Plotly**, **Streamlit**, and **SQLite/SQL**.

## Live dashboard
[Open the live dashboard](https://the-attention-lab-lin.streamlit.app/)

A closer look at content, audience and growth.

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

## Verified export totals
117 Reels; 5,323,019 account content views; 2,590,069 accounts reached.
Follower totals rise from 5,695 on July 25 to 13,162 on October 24: +7,467.
Daily net changes sum to +7,470 because the first row includes +3 against the prior day.

## Updating the dashboard
Changes are committed and pushed to this repository. Streamlit Community Cloud should track `main` and run `app.py`; a merged change then redeploys automatically. Feature branches and pull requests keep changes reviewable. GitHub access does not grant Streamlit account administration; verify the connected repository and branch in Streamlit settings if deployment does not update.

The dashboard uses a light theme, full-width desktop layout, four account KPI cards, and Overview, Content, Audience, and Methods & SQL tabs. Raw exports and SQL are retained unchanged.
