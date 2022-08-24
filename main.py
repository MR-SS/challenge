from itertools import count
from pydoc import cli
from typing import List
from router import user
from fastapi import Depends, FastAPI
from database import models
from database.models import Dbuser
from database.db import engine, get_db
from sqlalchemy.orm import Session
from database.hash import Hash


from database.db import init_database


init_database()
app = FastAPI()
app.include_router(user.router)
# app.include_router(authentication.router)
session = Session(engine)

# API Throttling
import redis

threshhold =10
period =20

def threshhold(key):
    req = redis.Redis(host="redis-server" ,db=0)
    if req.exists(key):
        req.set(key,1,ex=period)
    else :
        req.incr(key)
        count = int(req.get(key).decode())
        print("user total request",count)
        if count > threshhold:
            print ( "Blocked")
        else:
            pass



@app.get("/")
def read_root():
    return {"hello": "world"}
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
