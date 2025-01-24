from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from src.queries.book import get_book, create_book, update_book
from src.queries.bookmarks import get_bookmark
from src.serializers import Bookmark_Pydantic, Book_Pydantic


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['src.models']}
    )

    # await Tortoise.generate_schemas(safe=True)

    yield


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="src/templates")


@app.get('/bookmarks/{id}', response_class=HTMLResponse)
async def bookmarks(request: Request, id: str):
    bookmark = await get_bookmark(id)

    if not bookmark:
        return RedirectResponse(url='/', status_code=status.HTTP_404_NOT_FOUND)

    bookmark_serializer_obj = await Bookmark_Pydantic.from_tortoise_orm(bookmark)

    return templates.TemplateResponse(
        request=request,
        name="bookmarks.html",
        context=bookmark_serializer_obj.dict(),
    )


@app.get('/bookmarks/{id}/add', response_class=HTMLResponse)
async def add_book_form(request: Request, id: str):
    return templates.TemplateResponse(
        request=request,
        name="add_book.html",
        context={"id": id}
    )


@app.post('/bookmarks/{id}/add', response_class=RedirectResponse)
async def add_book(request: Request, id: str,  title: Annotated[str, Form()], current_page: Annotated[int, Form()], total_pages: Annotated[int, Form()]):
    await create_book(title, current_page, total_pages, id)

    return RedirectResponse(url=f'/bookmarks/{id}', status_code=status.HTTP_303_SEE_OTHER)


@app.get('/bookmarks/{id}/edit/{book_id}', response_class=HTMLResponse)
async def edit_book_form(request: Request, id: str, book_id: str):
    book = await get_book(book_id)

    if not book:
        return RedirectResponse(url='/', status_code=status.HTTP_404_NOT_FOUND)

    book_serializer_obj = await Book_Pydantic.from_tortoise_orm(book)

    return templates.TemplateResponse(
        request=request,
        name="edit_book.html",
        context={"id": id, "book": book_serializer_obj.dict()})


@app.post('/bookmarks/{id}/edit/{book_id}', response_class=RedirectResponse)
async def edit_book(request: Request, id: str, book_id: str, title: Annotated[str, Form()], current_page: Annotated[int, Form()], total_pages: Annotated[int, Form()]):
    await update_book(book_id, title, current_page, total_pages)

    return RedirectResponse(url=f'/bookmarks/{id}', status_code=status.HTTP_303_SEE_OTHER)
