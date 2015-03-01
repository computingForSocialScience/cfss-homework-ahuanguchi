import json, tweepy, string, time
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
    
    all_tweets = tweepy.Cursor(api.search, q=term, count=100, lang='en').items(17900)
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
            sentiment(tweet.text.replace(
                          'Death', ''
                      ).replace(
                          'death parade', 'parade'
                      ).replace(
                          'Assassination', ''
                      ).replace(
                          'assassination classroom', 'classroom'
                      ).replace(
                          'Cute', ''
                      ).replace(
                          'cute high', 'high'
                      ).encode('utf-8', 'ignore'))['compound'],
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
        
        # search_term = 'aldnoah'     # uncomment for different search terms to avoid breaking limit
        # search_term = 'akatsuki no yona'
        # search_term = 'durarara'
        # search_term = 'death parade'
        # search_term = 'rolling girls'
        search_term = 'sailor moon crystal'
        # search_term = 'yuri kuma'
        # search_term = 'assassination classroom'
        # search_term = 'koufuku graffiti'
        # search_term = 'cute high earth defense'
        
        tweets, entities = scrape_tweets(api, search_term)
        print('tweets: %s' % len(tweets))
        write_to_json('%s_tweets.json' % search_term.replace(' ', ''), tweets, entities)
        
    finally:
        stats = api.rate_limit_status()['resources']['search']['/search/tweets']
        print('remaining calls: %s' % stats['remaining'])
        print(time.localtime(stats['reset']))

