-- Run after: python build_database.py
-- SQL skills: aggregations, CTEs, joins, window functions.

-- 1) Weekly follower gains, week over week (window LAG).
WITH weekly AS (
  SELECT strftime('%Y-W%W',date) AS week, SUM(net_follower_change) AS net_new
  FROM followers GROUP BY 1
)
SELECT week, net_new, LAG(net_new) OVER (ORDER BY week) AS previous_week,
       net_new - LAG(net_new) OVER (ORDER BY week) AS wow_change
FROM weekly ORDER BY week;

-- 2) Daily post metrics alongside daily follower change (JOIN).
-- This is descriptive only: simultaneous daily association does NOT prove causation.
WITH daily_posts AS (
  SELECT SUBSTR(published_at,1,10) AS day, COUNT(*) AS reels,
         SUM(likes) AS likes, SUM(comments) AS comments
  FROM posts GROUP BY 1
)
SELECT f.date, f.net_follower_change, COALESCE(p.reels,0) AS reels_published,
       COALESCE(p.likes,0) AS likes_on_posts_published_that_day,
       COALESCE(p.comments,0) AS comments_on_posts_published_that_day
FROM followers f LEFT JOIN daily_posts p ON f.date = p.day ORDER BY f.date;
-- Note: cumulative likes at retrieval are NOT likes earned on publish date.

-- 3) Post ranking within month using ROW_NUMBER window function.
SELECT SUBSTR(published_at,1,7) AS month, published_at, caption, likes, comments,
       ROW_NUMBER() OVER (PARTITION BY SUBSTR(published_at,1,7)
                          ORDER BY likes DESC, post_id) AS rank_by_likes
FROM posts ORDER BY month, rank_by_likes;
