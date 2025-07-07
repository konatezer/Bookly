from fastapi import APIRouter, status, Depends
from typing import List
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
acces_token_bearer = AccessTokenBearer()

role_checker = Depends( RoleChecker(["admin", "user"]))


@book_router.get("/", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(acces_token_bearer),
):
    print(f"user login detail: {user_details}")
    books = await book_service.get_all_books(session)
    return books


@book_router.post(
    "/", status_code=201, response_model=Book, dependencies=[role_checker]
)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(acces_token_bearer),
) -> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.get("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(acces_token_bearer),
) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book uid: {book_uid} not found",
        )


@book_router.put("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(acces_token_bearer),
) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f" book uid: {book_uid} not found",
        )
    else:
        return updated_book


@book_router.delete("/{book_uid}", dependencies=[role_checker])
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(acces_token_bearer),
):
    book_to_delete = await book_service.delete_book(book_uid, session)
    print(f"Value of book before delete: {book_to_delete}")
    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The book uid: {book_uid} not found",
        )
    else:
        return f"The book uid: {book_uid}  has been deleted"
