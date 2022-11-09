import re
import json

import validation
import twitter
import service
import utils

def handler(event, context):
    print("Incoming event:")
    print(event)

    err_builder = utils.ErrorResponseBuilder(context.aws_request_id)

    if event['raw_path'] == "/":
        return generateTweetsRoute(err_builder, event)
    
    match = re.search(r'^/users/(.+)$', event['raw_path'])
    if match != None:
        return getUserRoute(err_builder, match.group(1))
    
    return err_builder.format_error_response(404, f"Path {event['raw_path']} not found")

def getUserRoute(err_builder, screenname):
    if err := validation.get_input_validation(screenname, err_builder):
        return err
    
    print(f"Fetching user details for @{screenname}")
    ret = twitter.get_user_details(screenname)
    if isinstance(ret, tuple):
        return err_builder.format_error_response(ret[0], ret[1])
    
    return ret

def generateTweetsRoute(err_builder, event):
    request = json.loads(event['body'])
    if err := validation.post_input_validation(request, err_builder):
        return err

    tweets = list()
    for user in request['users']:
        print(f"Fetching {user['count']} latest tweets from @{user['screenname']}...", flush=True)
        user_tweets = twitter.get_user_tweets(user['screenname'], user['count'])
        if isinstance(user_tweets, tuple):
            return err_builder.format_error_response(user_tweets[0], user_tweets[1])
        else:
            tweets += user_tweets

    # Remove stopwords, hyperlinks, etc..
    print("Running preprocess steps...", flush=True)
    tweets = service.preprocess(tweets)

    print("Building Markov model...", flush=True)
    P, n1_index_mapping, token_index_mapping = service.buildModel(tweets, request['N'])

    print("Generating tweets...", flush=True)
    newTweets = list()
    for _ in range(request['M']):
        newTweets.append(service.generateTweet(request['N'], P, n1_index_mapping, token_index_mapping))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "tweets": newTweets,
        })
    }
