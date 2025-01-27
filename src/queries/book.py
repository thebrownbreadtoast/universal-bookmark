from datetime import datetime
from tortoise import exceptions

from src.models import Book


async def get_book(id: str):
    try:
        return await Book.get(id=id)
    except exceptions.DoesNotExist:
        return None


async def create_book(title: str, current_page: int, total_pages: int, bookmark_id: str):
    return await Book.create(title=title, current_page=current_page, total_pages=total_pages, bookmark_id=bookmark_id)


async def update_book(bookmark_id: str, id: str, title: str, current_page: int, total_pages: int):
    book = await get_book(id)

    if not book:
        return None
    
    if str(book.bookmark_id) != bookmark_id:
        return None

    book.title = title
    book.current_page = current_page
    book.total_pages = total_pages

    await book.save()

    return book


async def destroy_book(bookmark_id: str, id: str):
    try:
        return await Book.get(id=id, bookmark_id=bookmark_id).delete()
    except exceptions.DoesNotExist:
        return None
