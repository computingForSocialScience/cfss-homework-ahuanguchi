import json, tweepy, string
from vaderSentiment.vaderSentiment import sentiment

# keys saved separately in gitignored file for security reasons
with open('auth.json', 'r') as f:
    saved = json.load(f)
consumer_key = saved['consumer_key']
consumer_secret = saved['consumer_secret']
access_token = saved['access_token']
access_token_secret = saved['access_token_secret']

def scrape_tweets(api, term):
    uppers = set(string.ascii_uppercase)
    
    all_tweets = tweepy.Cursor(api.search, q=term, count=100, until='2015-02-28', lang='en').items(18000)
    # all_tweets = tweepy.Cursor(api.user_timeline, screen_name=term, count=200).items()
    
    tweets_table = []
    entities_table = []
    
    for tweet in all_tweets:
        tweet_info = (
            tweet.id,
            tweet.text,
            str(tweet.created_at),
            tweet.place.full_name if tweet.place else None,
            tweet.favorite_count,
            tweet.retweet_count,
            term,
            sentiment(tweet.text.replace('#', '').encode('utf-8', 'ignore'))['compound'],
            int(
                all(
                    x[0] in uppers for x in tweet.text.split()
                    if x[0].isalpha() and '/' not in x
                )
            ),
            int(tweet.text.startswith('RT @'))
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

if __name__ == '__main__':
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    # print(api.rate_limit_status()['resources']['statuses']['/statuses/user_timeline'])
    # jaden_tweets, jaden_entities = scrape_tweets(api, 'officialjaden')
    # print(len(jaden_tweets))
    # write_to_json('jaden.json', jaden_tweets, jaden_entities)
    try:
        print(api.rate_limit_status()['resources']['search'])
        tweets, entities = scrape_tweets(api, 'Python')
        print(len(tweets))
        write_to_json('python_tweets.json', tweets, entities)
    finally:
        print(api.rate_limit_status()['resources']['search'])

