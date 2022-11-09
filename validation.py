import utils

def get_input_validation(request: dict, erb: utils.ErrorResponseBuilder):
    pass

def post_input_validation(request: dict, erb: utils.ErrorResponseBuilder):
    if not isinstance(request['N'], int):
        return erb.format_error_response(400, "Invalid value for N. Must be an integer in the range [2,6]")
    if request['N'] < 2:
        return erb.format_error_response(400, "Value of N cannot be less than 2")
    elif request['N'] > 6:
        return erb.format_error_response(400, "Value of N cannot be greater than 6, due to performance constraints. Values this high are also more likely to recreate existing tweets than create new ones.")
    
    if not isinstance(request['M'], int):
        return erb.format_error_response(400, "Invalid value for M. Must be an integer in the range [1,1000]")
    if request['M'] < 1:
        return erb.format_error_response(400, "Value of M must be at least 1 (We're here to generate at least one new tweet!)")
    if request['M'] > 1000:
        return erb.format_error_response(400, "Value of M must be at most 1000. Come on now. You don't need THAT many autogenerated tweets.")
    
    num_tweets_sum = 0
    for user in request['users']:
        if not isinstance(user['screenname'], str) or len(user['screenname']) > 15:
            return erb.format_error_response(400, f"Username @{user['screenname']} is not a valid Twitter username")
        if user["screenname"] == "":
            return erb.format_error_response(400, "Username cannot be blank")
        if not isinstance(user['count'], int):
            return erb.format_error_response(400, f"Invalid number of tweets to fetch for user @{user['screenname']}, should be an integer in the range [1,500]")
        num_tweets_sum += user['count']
    if num_tweets_sum < 1:
        return erb.format_error_response(400, "Total number of tweets to fetch across all requested users should be at least 1")
    if num_tweets_sum > 500:
        return erb.format_error_response(400, "Total number of tweets to fetch across all requested users must not be over 500")