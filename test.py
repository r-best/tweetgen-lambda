import json

import twitter
import service
import handler

from pprint import pprint

class MockLambdaContext:
    def __init__(self, aws_request_id: str) -> None:
        self.aws_request_id = aws_request_id

if __name__ == "__main__":
    req = {
        "users": [
            {
                "username": "ohnopodcast",
                "count": 200
            },
            # {
            #     "username": "",
            #     "count": 200
            # }
        ],
        "N": 2,
        "M": 10
    }

    res = handler.handler({ "body": json.dumps(req) }, MockLambdaContext(aws_request_id="abcd1234"))
    if res['statusCode'] != 200:
        print(res)
    else:
        print("----------")
        for tweet in json.loads(res['body'])["tweets"]:
            print(tweet)
            print("----------")
