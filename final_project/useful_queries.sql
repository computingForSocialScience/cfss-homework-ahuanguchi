USE cfss;

SELECT search_term, COUNT(*) AS num_tweets
FROM tweets
GROUP BY search_term
ORDER BY num_tweets DESC;

SELECT t1.search_term, (num_pos / num_neg) AS pos_neg_ratio
FROM (
    (
        SELECT search_term, COUNT(*) AS num_pos
        FROM tweets
        WHERE sentiment > 0
        GROUP BY search_term
    ) AS t1
    INNER JOIN (
        SELECT search_term, COUNT(*) AS num_neg
        FROM tweets
        WHERE sentiment < 0
        GROUP BY search_term
    ) AS t2
    ON t1.search_term = t2.search_term
)
ORDER BY pos_neg_ratio DESC;

SELECT search_term, AVG(sentiment) AS avg_sentiment
FROM tweets
GROUP BY search_term
ORDER BY avg_sentiment DESC;

SELECT search_term, AVG(sentiment) AS avg_pos_sentiment
FROM tweets
WHERE sentiment > 0
GROUP BY search_term
ORDER BY avg_pos_sentiment DESC;

SELECT search_term, AVG(sentiment) AS avg_neg_sentiment
FROM tweets
WHERE sentiment < 0
GROUP BY search_term
ORDER BY avg_neg_sentiment;

SELECT HOUR(created_at) AS hour_tweeted, AVG(sentiment) AS avg_sentiment
FROM tweets
GROUP BY hour_tweeted;

SELECT DAYOFWEEK(created_at) AS day_tweeted, AVG(sentiment) AS avg_sentiment
FROM tweets
GROUP BY day_tweeted;

SELECT DATE(created_at) AS day_tweeted, AVG(sentiment) AS avg_sentiment
FROM tweets
GROUP BY day_tweeted;

SELECT place, COUNT(*) AS num_tweets
FROM tweets
GROUP BY place
ORDER BY num_tweets DESC, place;

SELECT t1.place, COALESCE(t2.num, 0), COALESCE(t3.num, 0)
FROM (
    (
        SELECT place FROM tweets
        WHERE search_term IN ('durarara', 'shirobako')
        GROUP BY place
    ) AS t1
    LEFT OUTER JOIN (
        SELECT place, COUNT(*) AS num FROM tweets
        WHERE search_term = 'durarara'
        GROUP BY place
    ) AS t2
    ON t1.place = t2.place
    LEFT OUTER JOIN (
        SELECT place, COUNT(*) AS num FROM tweets
        WHERE search_term = 'shirobako'
        GROUP BY place
    ) AS t3
    ON t1.place = t3.place
);

SELECT search_term, (SUM(jaden_cap) / COUNT(*)) AS proportion_jadenlike
FROM tweets
GROUP BY search_term
ORDER BY proportion_jadenlike DESC;

SELECT search_term, (SUM(retweeted) / COUNT(*)) AS proportion_retweeted
FROM tweets
GROUP BY search_term
ORDER BY proportion_retweeted DESC;

SELECT search_term, AVG(retweet_count) AS avg_retweet_count
FROM tweets
GROUP BY search_term
ORDER BY avg_retweet_count DESC;

SELECT search_term, AVG(favorite_count) AS avg_favorite_count
FROM tweets
GROUP BY search_term
ORDER BY avg_favorite_count DESC;

SELECT
    search_term,
    AVG(num_hashtags) AS avg_num_hashtags
FROM (
    SELECT
        search_term,
        IF(
            hashtags LIKE '%,%',
            LENGTH(hashtags) - LENGTH(REPLACE(hashtags, ',', '')) + 1,
            IF(
                hashtags != '',
                1,
                0
            )
        ) AS num_hashtags
    FROM (
        tweets AS t
        INNER JOIN
        entities AS e
        ON t.id = e.id
    )
) AS full_table
GROUP BY search_term
ORDER BY avg_num_hashtags DESC;

SELECT
    search_term,
    AVG(num_urls) AS avg_num_urls
FROM (
    SELECT
        search_term,
        IF(
            urls LIKE '%,%',
            LENGTH(urls) - LENGTH(REPLACE(urls, ',', '')) + 1,
            IF(
                urls != '',
                1,
                0
            )
        ) AS num_urls
    FROM (
        tweets AS t
        INNER JOIN
        entities AS e
        ON t.id = e.id
    )
) AS full_table
GROUP BY search_term
ORDER BY avg_num_urls DESC;
