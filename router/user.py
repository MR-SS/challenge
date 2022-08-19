
from fastapi import Body, Depends, Path, Query, Response, APIRouter, Header, Request
from pydantic import BaseModel
from typing import Optional, List, Dict
from schemas import UserBase, UserDisplay, CouponCount
from database import db_user
from database.db import get_db
from database.db_user import get_all_users, make_gift
from auth.oauth2 import reusable_oath, decode_token


router = APIRouter(tags=['user'])

# create user


@router.post("/login", description="sign in  login")
def register_user(user: UserBase, db=Depends(get_db)):
    return db_user.login_user(db, user)


@router.get('/default')
def make_user(db=Depends(get_db)):
    return db_user.create_user(db)


# read All user
@router.get('/', response_model=List[UserDisplay])
def get_all_users(db=Depends(get_db)):  # ,token:str=Depends(oauth2_scheme)):
    return db_user.get_all_users(db)


# generate gift
@router.post("/generate-coupon", tags=["coupon"])
def generate_coupon(request: Request, count: CouponCount, db=Depends(get_db)):
    token = request.headers.get("Authrization")
    num = count.count
    user_auth = decode_token(token)
    if (user_auth["is_admin"] == True):
        return make_gift(num, db)
    else:
        return 'raise 403'
