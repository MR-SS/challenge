from sqlalchemy.orm.session import Session
from schemas import UserBase
from . import models
from database.hash import Hash
from database.models import Dbuser

def create_user(db:Session ,request:UserBase):
    user = Dbuser(
        username =request.username,
        password = Hash.bcrypt(request.password)

    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db:Session, request:UserBase):
    pass

def get_all_users(db:Session):
    return db.query(models.Dbuser).all()


def get_user(id, db:Session):
    return db.query(models.Dbuser).filter(models.Dbuser.id == id).first()

def get_user_by_username(username, db:Session):
    return db.query(models.Dbuser).filter(models.Dbuser.username == username).first()


def delete_user(id, db:Session):
    user = get_user(id, db)
    db.delete(user)
    db.commit()
    return 'ok'