import requests
import json

"""
first we create a token (id and secret key) for future request to reddit website.
For the token we created a developed application at - https://www.reddit.com/prefs/apps.
At the request we created a "secret" and "personal use script" to my account - "Dry_Policy1852"
The API for the script - kelly'sCiscoAPI
redirect uri- https://www.facebook.com/kelly.gudarna

I also created variables for the post request, link url and variables to filter with, in the subject
"""

SECRET = "ZXKMZcP-VrX1_IGP1SVlR74mZEIFsQ"
PERSONAL_USE_SCRIPT = "EMRf2Mqb4GVT5EsjCF_V2Q"
INIT_REDDIT = "https://oauth.reddit.com" #For post request
INIT_FOR_URL = "https://www.reddit.com" #For url link, in the final JSON
time_filter_in_subject = "all" #One of :hour, day, week, month, year, all
limit = 10 #The maximum number of items desired (default: 25, maximum: 100)


def get_headers():
    """
    Parameters:
    None

    Creating a header witch contains:
    The user-agent for thr HTTP request
    KellyAPI/0.0.1 to make an API client
    The request itself (the token)

    returns:
    a dict with the token
    """
    with open("password.txt", "r") as f:
        password = f.read()
    headers = {"User-Agent": "KellyAPI/0.0.1"}
    auth_token_val = requests.auth.HTTPBasicAuth(PERSONAL_USE_SCRIPT, SECRET)
    data = {
        "grant_type": "password",
        "username": "Dry_Policy1852",
        "password": password
    }
    request = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth_token_val, data=data, headers=headers)
    TOKEN = request.json()["access_token"]
    headers["Authorization"] = f"bearer {TOKEN}"
    return headers



def get_top_json_for_subreddit(subject, time_filter_in_subject, limit):
    """
    Parameters:
    The name of the subject
    time to filter in "top" (hour, day, week, month, year, all), Default is day
    limit of articles to show, default is 10

    first we are creating headers to work with
    Second we create a get request to - https://oauth.reddit.com/api/v1/me because it returns the preference settings of the logged in user
    Third, another get request to - https://oauth.reddit.com/r/{subject}/top so that we can filter on articles in top
    (for more info - https://www.reddit.com/dev/api#GET_api_v1_me , https://www.reddit.com/dev/api/#GET_top)

    finally, we create an empty dict to add all the important data, from each article, and turn it to a JSON

    returns:
    JSON that contains the top details of a posts from the subject
    """
    limit = int(limit)
    headers= get_headers()
    if(time_filter_in_subject not in ["hour", "day", "week", "month", "year", "all"]):
        result = {"ERROR" : f"{time_filter_in_subject} is not in [hour, day, week, month, year, all]"}
        return json.dumps(result, ensure_ascii=False)
    if(limit > 100 or limit < 0):
        result = {"ERROR": f"limit {limit} is not between 0 and 100"}
        return json.dumps(result, ensure_ascii=False)
    if not isinstance(limit, int):
        result=  {"ERROR": f"limit {limit} is not valid argument"}
        return json.dumps(result, ensure_ascii=False)
    requests.get(f"{INIT_REDDIT}/api/v1/me", headers=headers)
    params = {
        "t": time_filter_in_subject,
        "limit": limit
    }
    res = requests.get(f"{INIT_REDDIT}/r/{subject}/top", headers=headers, params=params)
    if(res.status_code != 200):
        result= {"ERROR": f"status code is {res.status_code}"}
        return json.dumps(result, ensure_ascii=False)
    top_posts = res.json()["data"]["children"]

    result = {}
    for i,post in enumerate(top_posts): #text in post
           result[f"post number {i+1}"] = {
            "id": post["data"]["id"],
            "title": post["data"]["title"],
            "url": f'{INIT_FOR_URL}{post["data"]["permalink"]}',
            "category": post["data"]["link_flair_text"],
            "user": post["data"]["author"],
            "text": post["data"]["selftext"],
            "ups": post["data"]["ups"],
            "upvote_ratio": post["data"]["upvote_ratio"],
            "thumbnail": post["data"]["thumbnail"],
            "creation_time": post["data"]["created"],
            "number_of_comments": post["data"]["num_comments"]
        }
    return json.dumps(result, ensure_ascii=False)