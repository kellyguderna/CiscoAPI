from back import *
from fastapi import FastAPI
import json
import requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn


app = FastAPI()

@app.get("/get")
def get_json(subreddit, time_filter_in_subject="day", limit=10):
    """
    Using fastAPI to get JSON from a subreddit at reddit

    Parameters:
    The name of the subject
    time to filter in "top" (hour, day, week, month, year, all), Default is day
    limit of articles to show, default is 10

    Returns:
    JSONResponse, The JSON response containing the data of top posts in the specific subject.
    """
    result = get_top_json_for_subreddit(subreddit, time_filter_in_subject, limit)
    return JSONResponse(content=json.loads(result))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
