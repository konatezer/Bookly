import uuid
from pydantic import BaseModel, Field
from datetime import datetime



class UserModel(BaseModel):

   uid: uuid.UUID 
   username: str
   email: str
   first_name: str
   last_name: str
   is_verified: bool 
   password_hash: str = Field(exclude=True)
   create_at: datetime 
   update_at: datetime 


class UserCreateModel(BaseModel):
   first_name: str = Field(max_length=40)
   last_name: str=  Field(max_length=40)
   username: str =  Field(max_length=8)
   email: str  = Field(max_length=40)
   password_hash: str = Field(min_length=6)


class UserLoginModel(BaseModel):
   email: str
   password_hash: str = Field(exclude=True)
