from fastapi import APIRouter, status
from typing import  List
from fastapi.exceptions import HTTPException

from src.books.book_data import books_list
from src.books.schemas import BookModel, BookUpdateModel


book_router = APIRouter()


@book_router.get("/", response_model=List[BookModel])
async def get_all_books():
   return books_list

@book_router.post("/", status_code=201)
async def create_a_book(book_data:BookModel) -> dict:
   new_book = book_data.model_dump()
   
   books_list.append(new_book)

   return new_book


@book_router.get("/{book_id}")
async def get_book(book_id:int) -> dict:
    for book in books_list:
        if book["id"] == book_id:
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"Book id {book_id} not found"
                        )


@book_router.put("/{book_id}")
async def update_book(book_id:int, book_update_data: BookUpdateModel) -> dict:
    for book in books_list:
         if book["id"] == book_id:
            book["title"]= book_update_data.title
            book["author"]= book_update_data.author
            book["publisher"]= book_update_data.publisher
            book["price"]= book_update_data.price
            book["rating"]= book_update_data.rating
            book["genre"]= book_update_data.genre
            book["page_count"]= book_update_data.page_count
            book["language"]= book_update_data.language

            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f" book id: {book_id} not found"
                        )

@book_router.delete("/{book_id}")
async def delete_book(book_id:int) :
    for book in books_list:
        if book["id"] == book_id:
            books_list.remove(book)
            
            return f"The book id: {book_id} has been removed"
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"The book id: {book_id} not found"
                        )



