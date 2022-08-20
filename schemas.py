from ast import Str
from datetime import time
from itertools import count
from re import S
from typing import List
from xmlrpc.client import Boolean, boolean
from pydantic import BaseModel



class UserBase(BaseModel):
    username: str
    password: str
    
class CouponCount(BaseModel):
     count : int


class UserDisplay(BaseModel):
    username:str
    password:str
    is_admin :bool

    class Config:
        orm_mode = True

class CouponDisplay(BaseModel):
    code : str
    validate_from : time
    validate_to : time
    active : bool
    
    class Config:
        orm_mode = True


class CouponBase(BaseModel):
    code :str
    active:bool
class Valid_coupon(BaseModel):
    code : str