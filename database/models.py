from email.policy import strict
from enum import unique
import string
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base

Base  = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id  = Column(Integer, primary_key=True, unique=True)
    username = Column("name",string(50))
    password = Column(Float)
    role = Column(DateTime(timezone=True), server_default=func.now())



class Coupon(Base):
    __tablename__ = 'coupons'

    id = Column(Integer, primary_key=True)
    validate_from= Column(DateTime(timezone=True), server_default=func.now())
    validate_to = Column(DateTime(timezone=True), server_default=func.now())
    active = Column()
    
