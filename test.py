import json

import twitter
import service
import handler

from pprint import pprint

class MockLambdaContext:
    def __init__(self, aws_request_id: str) -> None:
        self.aws_request_id = aws_request_id

def testGenerateTweets():
    req = {
        "users": [
            {
                "screenname": "ohnopodcast",
                "count": 100
            },
            {
                "screenname": "carriepoppyYES",
                "count": 100
            }
        ],
        "N": 3,
        "M": 20
    }

    res = handler.handler({
        "rawPath": "/",
        "body": json.dumps(req)
        }, MockLambdaContext(aws_request_id="abcd1234"))
    if res['statusCode'] != 200:
        print(res)
    else:
        print("----------")
        for tweet in json.loads(res['body'])["tweets"]:
            print(tweet)
            print("----------")

def testGetUser():
    screenname = "verflaree"

    res = handler.handler({
        "rawPath": f"/users/{screenname}"
        }, MockLambdaContext(aws_request_id="abcd1234"))
    print(res)

if __name__ == "__main__":
    # testGenerateTweets()
    testGetUser()
