from tortoise import exceptions

from src.models import Book


async def get_book(id: str):
    try:
        return await Book.get(id=id)
    except exceptions.DoesNotExist:
        return None


async def create_book(title: str, current_page: int, total_pages: int, bookmark_id: str):
    return await Book.create(title=title, current_page=current_page, total_pages=total_pages, bookmark_id=bookmark_id)


async def update_book(id: str, title: str, current_page: int, total_pages: int):
    return await Book.filter(id=id).update(title=title, current_page=current_page, total_pages=total_pages)
