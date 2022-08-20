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


@app.get("/")
def read_root():
    return {"hello": "world"}
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
