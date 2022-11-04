import os
import tweepy

def authenticate():
    auth = tweepy.OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret'])
    auth.set_access_token(os.environ['access_token_key'], os.environ['access_token_secret'])
    return tweepy.API(auth)
twitter_api = authenticate()

@profile
def get_user_tweets(username, num_tweets):
    try:
        tweets = []
        for tweet in tweepy.Cursor(twitter_api.user_timeline, screen_name=username, include_rts=False, trim_user=True, tweet_mode='extended', count=100).items(num_tweets):
            tweets.append(tweet.full_text)
            # print(tweet.full_text)
        print(len(tweets))
        return tweets
    except tweepy.errors.TooManyRequests:
        return "Whoops, rate limit exceeded!"
    except tweepy.errors.TweepyException as err:
        print(err.message[0]['message'])
        return []
