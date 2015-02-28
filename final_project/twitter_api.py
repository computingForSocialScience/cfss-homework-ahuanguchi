import json, tweepy

# keys saved separately in gitignored file for security reasons
with open('auth.json', 'r') as f:
    saved = json.load(f)
consumer_key = saved['consumer_key']
consumer_secret = saved['consumer_secret']
access_token = saved['access_token']
access_token_secret = saved['access_token_secret']

def scrape_tweets(api, name):
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
        tweet_info = []
        tweet_info.append(tweet.id)
        tweet_info.append(tweet.text)
        tweet_info.append(str(tweet.created_at))
        tweet_info.append(tweet.place)
        tweet_info.append(tweet.favorite_count)
        tweet_info.append(tweet.retweet_count)
        tweet_info.append('')       # placeholder for sentiment
        tweet_info.append(name)
        extra_info = []
        extra_info.append(tweet.id)
        extra_info.append([x['text'] for x in tweet.entities['hashtags']])
        extra_info.append([x['screen_name'] for x in tweet.entities['user_mentions']])
        extra_info.append([x['url'] for x in tweet.entities['urls']])
        
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
    
    jaden_tweets, jaden_entities = scrape_tweets(api, 'officialjaden')
    write_to_json('jaden.json', jaden_tweets, jaden_entities)
