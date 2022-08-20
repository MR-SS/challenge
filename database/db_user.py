from sqlalchemy.orm.session import Session
from schemas import UserBase, CouponCount
from . import models
from database.hash import Hash
from database.models import Dbuser
from database import db_coupon
from sqlalchemy.sql import exists
from auth import oauth2
import random
from fastapi import Depends


def create_user(db: Session):
    db.add(Dbuser(
        username="admin",
        password=Hash.bcrypt("admin"),
        is_admin=True
    ))

    db.add(Dbuser(
        username="sajjad",
        password=Hash.bcrypt("123"),
        is_admin=False

    ))
    db.commit()


# login user
def login_user(db: Session, request: UserBase):
    username = request.username
    password = request.password

    user_object = db.query(Dbuser).filter_by(username=username).first()
    if (user_object == None):
        return (" Not Vaild username or Poassword")
    else:
        db_hashed_password = user_object.password
        if Hash.verify(db_hashed_password, password):
            is_admins = user_object.is_admin
            return (oauth2.get_token(username, is_admins))
        else:
            return ("Not Vaild username or Poassword")


def get_all_users(db: Session):
    return db.query(models.Dbuser).all()

# def get_user(id, db:Session):
#     return db.query(models.Dbuser).filter(models.Dbuser.id == id).first()


def get_user_by_username(username, db: Session):
    return db.query(models.Dbuser).filter(models.Dbuser.username == username).first()


def make_gift(count: int, db: Session):
    coupons = []
    for i in range(count):
        randm_number = random.randint(1000, 9999)
        '''
            Coupon codes must be UNIQUE
        '''
        coupon = db_coupon.add_coupon(randm_number, db)
        coupons.append({
            'id': coupon.id,
            'code': coupon.code
        })
    return coupons


'''
router.py api == controller
models ==> db
'''
