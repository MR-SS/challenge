from http.client import HTTPException
from itertools import count
from logging import exception
from pydoc import cli
from typing import List
from router import user
from fastapi import Depends, FastAPI ,Request
from database import models
from database.models import Dbuser
from database.db import engine, get_db
from sqlalchemy.orm import Session
from database.hash import Hash
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from database.db import init_database
import logging


init_database()
app = FastAPI()
app.include_router(user.router)
# app.include_router(authentication.router)
session = Session(engine)

@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.handlers.RotatingFileHandler("api.log",mode="a",maxBytes = 100*1024, backupCount = 3)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
# API Throttling
import redis


@app.middleware("http")
async def limit_api_call(request: Request ,call_next):
    # try:
    key = request.client.host
    threshhold =20
    period =1
    print ("sallam")
    req = redis.Redis(host="redis" ,db=0)
    if  not req.exists(key):
        req.set(key,1,ex=period)
    else :
        req.incr(key)
        count = int(req.get(key).decode())
        print("user total request",count)
        if count > threshhold:
            return JSONResponse(status_code=429,content={'reason': str("api limiting")}) 
        else:
            pass
    response = await call_next(request)
    return response





@app.get("/")
def read_root():
    return {"hello": "world"}
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
