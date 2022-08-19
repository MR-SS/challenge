from urllib import request
from sqlalchemy.orm.session import Session
from schemas import CouponBase, CouponCount
from . import models
from database.hash import Hash
from database.models import Dbcoupon, Dbuser
from auth import oauth2
import random
from fastapi import Depends


def add_coupon(random_number: int, db: Session):
    print(random_number)

    coupon = Dbcoupon(
        code=random_number,
        active=True
    )
    db.add(coupon)
    db.commit()
    return coupon
