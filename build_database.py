"""Build a local SQLite database from the original Muse CSV exports."""
from pathlib import Path
import sqlite3
import pandas as pd
ROOT=Path(__file__).parent
with sqlite3.connect(ROOT/'attention_lab.sqlite') as con:
    for name, file in [('posts','instagram_posts_2026-07-25_to_2026-10-25.csv'),('followers','instagram_follower_growth_daily.csv'),('account_totals','instagram_account_totals_2026-07-25_to_2026-10-25.csv'),('demographics','instagram_audience_demographics.csv')]:
        pd.read_csv(ROOT/'data'/file).to_sql(name,con,if_exists='replace',index=False)
print('Created attention_lab.sqlite')
