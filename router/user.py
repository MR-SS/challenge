
from fastapi import Body, Depends, Path, Query, Response, APIRouter, Header, Request
from pydantic import BaseModel
from typing import Optional, List, Dict
from schemas import UserBase, UserDisplay, CouponCount, Valid_coupon
from database import db_user
from database.db import get_db
from database.db_user import get_all_users, make_gift
from auth.oauth2 import reusable_oath, decode_token
from database.models import User_transaction
from fastapi.exceptions import HTTPException



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
    if token == None :
        raise HTTPException(401,"no authorize header")
    num = count.count
    user_auth = decode_token(token)
    if (user_auth["is_admin"] == True):
        return make_gift(num, db)
    else:
        raise HTTPException(401,"Not Authorize user!!")
        
@router.post("/submit-coupon", tags=["coupon"])
def submit_coupon(request:Request,coupon: Valid_coupon ,db=Depends(get_db)):
    code = coupon.code
    '''
        can check only users can add coupon
    '''
    token = request.headers.get("Authrization")
    if token == None :
        raise HTTPException(401,"no authorize header")
    user_auth = decode_token(token)
    user_object = db.query(User_transaction).filter_by(user_id=user_auth["username"]).first()
    if( user_object == None):
        # print("mitooni")
        def add_transaction(username,code:int, db=Depends(get_db)):
            coupon_winner = db.query(User_transaction).filter_by(user=user_auth["username"]).first()
            db.add(User_transaction(
                user = coupon_winner,
                code = code
            ))
            db.commit()
            return  db.query(User_transaction).all()
        return add_transaction(user_auth["username"],code,db)
        '''
            RACE CONDITION
        '''

    else:
        print ("nmitooni")

