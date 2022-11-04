import twitter
import service

def handler(event, context):
    tweets = list()
    for user in event['users']:
        print(f"Fetching {user['count']} latest tweets from @{user['username']}...", flush=True)
        tweets += twitter.get_user_tweets(user['username'], user['count'])

    # Remove stopwords, hyperlinks, etc..
    print("Running preprocess steps...", flush=True)
    tweets = service.preprocess(tweets)

    print("Building Markov model...", flush=True)
    P, n1_index_mapping, token_index_mapping = service.buildModel(tweets, event['N'])

    print("Generating tweets...", flush=True)
    newTweets = list()
    for _ in range(event['M']):
        newTweets.append(service.generateTweet(event['N'], P, n1_index_mapping, token_index_mapping))

    res = {
        "tweets": newTweets,
    }
    return res
