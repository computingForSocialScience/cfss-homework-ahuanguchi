USE cfss;

DROP TABLE IF EXISTS tweets;
CREATE TABLE tweets (
    id BIGINT,
    tweet_text VARCHAR(200) CHARACTER SET utf8mb4,
    created_at DATETIME,
    place VARCHAR(100),
    favorite_count INT UNSIGNED,
    retweet_count INT UNSIGNED,
    search_term VARCHAR(100),
    sentiment DECIMAL(5, 4),
    jaden_cap TINYINT(1),
    retweeted TINYINT(1),
    INDEX (id),
    INDEX (search_term),
    INDEX (created_at),
    INDEX (place),
    INDEX (sentiment)
);

DROP TABLE IF EXISTS entities;
CREATE TABLE entities (
    id BIGINT,
    hashtags VARCHAR(140),
    urls VARCHAR(140),
    user_mentions VARCHAR(140),
    PRIMARY KEY (id)
);
