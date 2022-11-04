import twitter
import service

def handler(event, context):
    tweets = list()
    for user in event.Users:
        tweets += twitter.get_user_tweets(user)

    # Remove stopwords, hyperlinks, etc..
    tweets = service.preprocess(tweets)

    P, tokens = service.buildModel(tweets, event.N)

    newTweets = list()
    for _ in range(event.M):
        newTweets.append(service.generateTweets(event.M, event.N, P, tokens))

    res = {
        "tweets": newTweets,
    }
    return res
