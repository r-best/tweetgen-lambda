import json

import twitter
import service
import handler

from pprint import pprint

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

    res = handler.handler({ "body": json.dumps(req) }, { "aws_request_id": "abcd1234" })
    if res['statusCode'] != 200:
        print(res)
    else:
        print("----------")
        for tweet in json.loads(res['body'])["tweets"]:
            print(tweet)
            print("----------")
