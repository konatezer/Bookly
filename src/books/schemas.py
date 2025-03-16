from datetime import date, datetime
import uuid
from pydantic import BaseModel

class Book(BaseModel):
        uid: uuid.UUID
        title: str
        author:  str
        publisher: str
        publication_date: date
        price: float
        rating: float
        genre: str
        page_count: int
        language: str
        create_at: datetime
        update_at: datetime

class BookCreateModel(BaseModel):
        title: str
        author:  str
        publisher: str
        publication_date: str
        price: float
        rating: float
        genre: str
        page_count: int
        language: str
   

class BookUpdateModel(BaseModel):
        title: str
        author:  str
        publisher: str
        publication_date: date
        price: float
        rating: float
        genre: str
        page_count: int
        language: str
   