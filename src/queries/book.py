from tortoise import exceptions

from src.models import Book, BookLog
from src.queries.bookmarks import update_last_read


async def get_book(id: str):
    try:
        return await Book.get(id=id)
    except exceptions.DoesNotExist:
        return None


async def create_book(title: str, current_page: int, total_pages: int, bookmark_id: str):
    book = await Book.create(title=title, current_page=current_page, total_pages=total_pages, bookmark_id=bookmark_id)

    if current_page:
        await update_last_read(bookmark_id)

    return book


async def create_book_log(book_id: str, start_page: int, end_page: int, note: str = ""):
    return await BookLog.create(book_id=book_id, start_page=start_page, end_page=end_page, note=note)


async def update_book(bookmark_id: str, id: str, title: str, current_page: int, total_pages: int, note: str = ""):
    book = await get_book(id)

    if not book:
        return None
    
    if str(book.bookmark_id) != bookmark_id:
        return None

    await create_book_log(id, book.current_page, current_page, note)

    book.title = title
    book.current_page = current_page
    book.total_pages = total_pages

    await book.save()

    await update_last_read(bookmark_id)

    return book


async def destroy_book(bookmark_id: str, id: str):
    try:
        return await Book.get(id=id, bookmark_id=bookmark_id).delete()
    except exceptions.DoesNotExist:
        return None
