import logging
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .utils import decode_token


class AccesTokenBearer(HTTPBearer):
   
   def __init(self, auto_error = True):
      super().__init__(auto_error=auto_error)


   async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
      creds = await  super().__call__(request)
      
      # print(f"credential schema: {creds.scheme}")
      # print(f"credential info: {creds.credentials}")
    
      token = creds.credentials
      token_data = decode_token(token)

      #logging.debug(f"token_data: {token_data}")

      if not self.token_valid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inval or expired token")
      
      if token_data['refresh']:
           raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token")

      return token_data

   def token_valid(self, token: str) -> bool:

      token_data = decode_token(token)

      return True if token_data is not None else False