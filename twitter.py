import os
import tweepy

def authenticate():
    auth = tweepy.OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret'])
    auth.set_access_token(os.environ['access_token_key'], os.environ['access_token_secret'])
    return tweepy.API(auth)
twitter_api = authenticate()

def get_user_tweets(username, num_tweets):
    try:
        tweets = []
        for tweet in tweepy.Cursor(twitter_api.user_timeline, screen_name=username, include_rts=False, trim_user=True, tweet_mode='extended', count=100).items(num_tweets):
            tweets.append(tweet.full_text)
        return tweets
    except tweepy.TooManyRequests:
        return (429, "Rate limit exceeded")
    except tweepy.NotFound:
        return (400, f"User @{username} cannot be found")
    except tweepy.Unauthorized:
        return (400, f"Cannot fetch tweets of @{username}, are they a private account?")
    except tweepy.TweepyException as e:
        print(e)
        return (500, "Unknown error, try again later")
