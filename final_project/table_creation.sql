USE cfss;

DROP TABLE IF EXISTS tweets;
CREATE TABLE tweets (
    id BIGINT,
    tweet_text VARCHAR(140),
    created_at DATETIME,
    place VARCHAR(40),
    favorite_count INT UNSIGNED,
    retweet_count INT UNSIGNED,
    sentiment DOUBLE,
    search_term VARCHAR(20),
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS entities;
CREATE TABLE entities (
    id BIGINT,
    hashtags VARCHAR(140),
    urls VARCHAR(140),
    user_mentions VARCHAR(140),
    PRIMARY KEY (id)
);
