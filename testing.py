import requests
import json

if __name__ == "__main__":
    print("Test number 1: checking that values return")
    r = requests.get("http://0.0.0.0:8000/get?subreddit=Kiteboarding&limit=4&time_filter_in_subject=all")
    result = json.loads(r.text)
    for post_id in result:
        print(post_id)
        for key in result[post_id]:
            print(f"\t{key}: {result[post_id][key]}")

    print("*"*20)
    print("Test number 2: limit not in range")
    r = requests.get("http://0.0.0.0:8000/get?subreddit=Kiteboarding&limit=-3&time_filter_in_subject=all")
    result = json.loads(r.text)
    print(result)

    print("*"*20)
    print("Test number 3: time not in list of valid values")
    r = requests.get("http://0.0.0.0:8000/get?subreddit=Kiteboarding&limit=3&time_filter_in_subject=minute")
    result = json.loads(r.text)
    print(result)

