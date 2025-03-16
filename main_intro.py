from fastapi import FastAPI, Header 
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


user_list = [
    "Sidi",
    "Alpha",
    "Amadou",
    "Ali",
    "Souleyman"
]

book_list = [
    {
        "id": "1",
        "title": "Book 1",
        "author": "Author 1",
        "publisher": "Publisher 1",
        "publication_date": "2010-01-01",
        "price": 20.99,
        "rating": 4.5,
        "genre": "Fiction",
        "page_count": 1234,
        "language": "English"
    },
    {
        "id": "2",
        "title": "Book 2",
        "author": "Author 2",
        "publisher": "Publisher 2",
        "publication_date": "2020-02-02",
        "price": 15.99,
        "rating": 4.2,
        "genre": "Non-Fiction",
        "page_count": 2345,
        "language": "French"
    }
    {
        "id": "3",
        "title": "Book 3",
        "author": "Author 3",
        "publisher": "Publisher 3",
        "publication_date": "2021-03-03",
        "price": 18.99,
        "rating": 4.7,
        "genre": "Fiction",
        "page_count": 3456,
        "language": "Spanish"
    }
   
]

@app.get('/')
def ping():
    return {"message": "Pong!"}

@app.get('/greet/{name}')
async def greet_name(name: str) -> dict:
    return {"Message": f"Hello, {name}"}

@app.get('/greet_qeury')
async def greet_query(country: str = "Mali", language: str = "Bambara") -> dict:
    return  {
        "Message": f"Hello, {country or 'Mali'} speak {language}"
    }

@app.get('/greet_path_qeury/{name}')
async def greet_age(name: str, age: int) -> dict:
    return {"Message": f"Hello, {name}! You are {age} years old"}
      

@app.get('/greet_path_qeury_optional/')
async def greet_age(name: Optional[str] = "User", age: int = 0) -> dict:
    return {"Message": f"Hello, {name}! You are {age} years old"}


class bookCreateModel(BaseModel):
    title: str
    author: str

# request body
@app.post('/create_book')
async def create_book(book_data: bookCreateModel):
    return{
        "title":book_data.title,
        "author": book_data.author,
        "message": "Book created successfully"
    }


@app.get('/get_headers')
async def get_headers(
    accept:str = Header(None),
    content_type:str = Header(None)
):
    request_headers = {}
    request_headers["Accept"] =  accept 
    request_headers["Content-Type"] = content_type  

    return request_headers

@app.get('/search_users')
async def search_user(username:str):
    # Simulate a database query
    if username in user_list:
        return {"message": f"{username} found in the user list"}
    else:
        return {"message": f"{username} not found in the user list"}