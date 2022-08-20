from .hash import Hash
from enum import unique
from unicodedata import name
from sqlalchemy.sql import func
from typing import List
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database.db import Base
from sqlalchemy.orm.session import Session 
from .db import engine

Base = declarative_base()
class Dbuser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column('username', String(50), unique=True)
    password = Column('password', String)
    is_admin = Column(Boolean, default=False)
    buyer = relationship("User_transaction", back_populates="user")


class Dbcoupon(Base):
    __tablename__ = 'coupons'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True)
    validate_from = Column(DateTime(timezone=True), server_default=func.now())
    validate_to = Column(DateTime(timezone=True), server_default=func.now())
    active = Column(Boolean)
    bcopon = relationship("User_transaction", back_populates="ticket")


class User_transaction(Base):
    __tablename__ = "userTransactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Dbuser", back_populates="buyer")
    coupon_id = Column(Integer, ForeignKey("coupons.id"))
    ticket = relationship("Dbcoupon", back_populates="bcopon")

