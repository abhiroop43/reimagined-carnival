import datetime
import json
from typing import Optional

from bson import ObjectId
from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
from uuid import uuid4
from pymongo import MongoClient
from pprint import pprint

app = FastAPI()

def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__

class Candidate(BaseModel):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    name: str
    vendor: str
    cv_received_date: datetime.datetime
    availability: int = 30


try:
    client = MongoClient("mongodb://localhost:27017")
    db = client.recruitment
    # db = client.admin
    # # Issue the serverStatus command and print the results
    # serverStatusResult = db.command("serverStatus")
    # pprint(serverStatusResult)
except:
    print('Database connection failed')


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/candidates")
def get_posts():
    candidates = db.candidates.find()
    return {"data": candidates}


# @app.get("/posts/latest")
# def get_latest_post():
#     return {"data": my_posts[-1]}


@app.get("/candidates/{id}")
def get_post(candidate_id: str):
    print(candidate_id)
    candidate = db.candidates.find_one({_id: ObjectId(candidate_id)})
    # post = [x for x in my_posts if x["id"] == post_id]

    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with id: {post_id} was not found")

    return {"data": candidate}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(candidate: Candidate):
    # data = candidate.__dict__
    jarray = candidate.toJSON()
    db.candidates.insert_one(jarray)

    return {"data": candidate}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(post_id):
#     post_to_be_deleted = get_post(post_id)["data"][0]
#
#     my_posts.remove(post_to_be_deleted)
#
#     #    return {"data": post_to_be_deleted}
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#
#
# @app.put("/posts/{id}")
# def update_post(post_id: str, post: Post):
#     existing_post = get_post(post_id)["data"][0]
#
#     existing_post["title"] = post.title
#     existing_post["content"] = post.content
#     existing_post['rating'] = str(post.rating)
#
#     return {"data": existing_post}
