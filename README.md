# CiscoAPI
This API was designed to get top posts from reddit website, using filter such as subredit, time and amount of posts.
In order to use the app you need to run the front.py file and than you can use get request with the following format:

http://0.0.0.0:8000/get?subreddit=
<subreddit>&limit=<int between 0 to 100>&time_filter_in_subject=<choose a time from: hour, day, week, month, year, all>

The API returns the requested JSON with the filtered data.
