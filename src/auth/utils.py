from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status
from passlib.context import CryptContext
import jwt
import uuid
from src.config import ConfigAccessEnvVarriable


password_contect = CryptContext(
   schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
   hash = password_contect.hash(password)

   return hash

def verify_password(password: str, hash: str) -> bool:
   return password_contect.verify(password , hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
   payload = {
      "user": user_data,
      "exp": int((datetime.now(timezone.utc) + (expiry or timedelta(seconds=ACCESS_TOKEN_EXPIRY))).timestamp()),
      "jti": str(uuid.uuid4()),
      "refresh": refresh
   }

   token = jwt.encode(
      payload=payload,
      key=ConfigAccessEnvVarriable.JWT_SECRET,
      algorithm=ConfigAccessEnvVarriable.JWT_ALGORITHM
   )

   return token



def decode_token(token: str ) -> dict:
   try:
      token_data = jwt.decode(
         jwt=token,
         key=ConfigAccessEnvVarriable.JWT_SECRET,
         algorithms=[ConfigAccessEnvVarriable.JWT_ALGORITHM]
      )
      return token_data
   except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
   except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")