
# from fastapi.exceptions import HTTPException
# from fastapi import  status ,Depends
# from database.db import get_db
# from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
# from typing import Optional
from datetime import timedelta, timezone ,datetime
from time import sleep
from jose import jwt ,JWTError,JOSEError
from fastapi.exceptions import HTTPException


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# #make it with openssl rand -hex 32
SECRET_KEY = '6c7d438d2ea66cc11ee315566bda6f45336930dc2a40eaa96ec009524c20aa69'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30



reusable_oath = OAuth2PasswordBearer(
tokenUrl="/login",
scheme_name="JWT"

)

def get_token(username,is_admin):
  info = {
    "username":username,
    "is_admin":is_admin,
    "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  }
  encoded = jwt.encode(info, SECRET_KEY, ALGORITHM)

  return {
        'access_token': encoded,
        'type_token': 'bearer'
    }
  

def decode_token(token):
  try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return decoded
  except JOSEError:
     raise HTTPException(401)
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#   to_encode = data.copy()
#   if expires_delta:
#     expire = datetime.utcnow() + expires_delta
#   else:
#     expire = datetime.utcnow() + timedelta(minutes=15)
#   to_encode.update({"exp": expire})
#   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  
#   return encoded_jwt


# def get_current_user(token: str=Depends(oauth2_scheme), db: Session= Depends(get_db)):
#   error_credential = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                    detail='invalid credentials',
#                                    headers={'WWW-authenticate': 'bearer'})

#   try:
#     _dict = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
#     username = _dict.get('sub')
#     if not username:
#       raise error_credential
#   except JWTError:
#     raise error_credential

#   user = get_user_by_username(username, db)

#   return user