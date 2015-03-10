USE cfss;

SELECT search_term, COUNT(*) as num_tweets
FROM tweets
GROUP BY search_term
ORDER BY num_tweets DESC;

SELECT t1.search_term, (num_pos / num_neg) as pos_neg_ratio
FROM (
    (
        SELECT search_term, COUNT(*) as num_pos
        FROM tweets
        WHERE sentiment > 0
        GROUP BY search_term
    ) AS t1
    INNER JOIN (
        SELECT search_term, COUNT(*) as num_neg
        FROM tweets
        WHERE sentiment < 0
        GROUP BY search_term
    ) AS t2
    ON t1.search_term = t2.search_term
)
ORDER BY pos_neg_ratio DESC;

SELECT search_term, AVG(sentiment) as avg_sentiment
FROM tweets
GROUP BY search_term
ORDER BY avg_sentiment DESC;

SELECT search_term, AVG(sentiment) as avg_pos_sentiment
FROM tweets
WHERE sentiment > 0
GROUP BY search_term
ORDER BY avg_pos_sentiment DESC;

SELECT search_term, AVG(sentiment) as avg_neg_sentiment
FROM tweets
WHERE sentiment < 0
GROUP BY search_term
ORDER BY avg_neg_sentiment;

SELECT HOUR(created_at) as hour_tweeted, AVG(sentiment) as avg_sentiment
FROM tweets
GROUP BY hour_tweeted;

SELECT DAYOFWEEK(created_at) as day_tweeted, AVG(sentiment) as avg_sentiment
FROM tweets
GROUP BY day_tweeted;

SELECT place, COUNT(*) as num_tweets
FROM tweets
GROUP BY place
ORDER BY num_tweets DESC, place;

SELECT t1.place, COALESCE(t2.num, 0), COALESCE(t3.num, 0) FROM (
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
