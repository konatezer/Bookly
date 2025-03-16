from pydantic import BaseModel

class BookModel(BaseModel):
        id: int
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
        price: float
        rating: float
        genre: str
        page_count: int
        language: str
   