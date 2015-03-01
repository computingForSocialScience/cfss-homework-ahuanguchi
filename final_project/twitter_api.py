import json, tweepy, string, pymysql
from vaderSentiment.vaderSentiment import sentiment

# keys saved separately in gitignored file for security reasons
with open('auth.json', 'r') as f:
    saved = json.load(f)
consumer_key = saved['consumer_key']
consumer_secret = saved['consumer_secret']
access_token = saved['access_token']
access_token_secret = saved['access_token_secret']

def scrape_tweets(api, name):
    uppers = set(string.ascii_uppercase)
    special_chars = ('#', '@', '/')
    
    user_tweets = []
    tweets = api.user_timeline(screen_name=name, count=200)
    user_tweets.extend(tweets)
    limit_id = user_tweets[-1].id - 1
    while True:
        tweets = api.user_timeline(screen_name=name, count=200, max_id=limit_id)
        if len(tweets) == 0:
            break
        user_tweets.extend(tweets)
        limit_id = user_tweets[-1].id - 1
    
    tweets_table = []
    entities_table = []
    
    for tweet in user_tweets:
        tweet_info = (
            tweet.id,
            tweet.text,
            str(tweet.created_at),
            tweet.place,
            tweet.favorite_count,
            tweet.retweet_count,
            name,
            sentiment(tweet.text.replace('#', '').encode('utf-8', 'ignore'))['compound'],
            int(
                all(
                    x[0] in uppers for x in tweet.text.split() if all(
                        y not in x for y in special_chars
                    )
                )
            ),
            int(bool(tweet.startswith('RT @')))
        )
        extra_info = (
            tweet.id,
            [x['text'] for x in tweet.entities['hashtags']],
            [x['screen_name'] for x in tweet.entities['user_mentions']],
            [x['url'] for x in tweet.entities['urls']]
        )
        tweets_table.append(tweet_info)
        entities_table.append(extra_info)
    
    return tweets_table, entities_table

def write_to_json(filename, tweets_table, entities_table):
    with open(filename, 'w') as f:
        dct = {'tweets_table': tweets_table, 'entities_table': entities_table}
        json.dump(dct, f)

def write_to_mysql(cursor, tweets_table, entities_table):
    pass

if __name__ == '__main__':
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    jaden_tweets, jaden_entities = scrape_tweets(api, 'officialjaden')
    write_to_json('jaden.json', jaden_tweets, jaden_entities)
