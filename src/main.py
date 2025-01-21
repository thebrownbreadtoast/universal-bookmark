from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from tortoise import Tortoise


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['src.models.books', 'src.models.bookmarks']}
    )

    await Tortoise.generate_schemas()

    yield


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="src/templates")


@app.get('/bookmarks/{id}', response_class=HTMLResponse)
async def bookmarks(request: Request, id: str):
    return templates.TemplateResponse(
        request=request,
        name="bookmarks.html",
        context={
            "id": 1,
            "books": [
                {"id": 1, "title": "Kane & Able", "current_page": 100, "total_pages": 200, "modified_at": "2025-01-18"},
                {"id": 2, "title": "Shoe Dog", "current_page": 15, "total_pages": 299, "modified_at": "2025-01-21"},
            ]
        }
    )


@app.get('/bookmarks/{id}/add', response_class=HTMLResponse)
async def add_bookmark_form(request: Request, id: str):
    return templates.TemplateResponse(request=request, name="add_book.html")


@app.post('/bookmarks/{id}/add', response_class=RedirectResponse)
async def add_bookmark(request: Request, id: str):
    return RedirectResponse(url=f'/bookmarks/{id}', status_code=status.HTTP_303_SEE_OTHER)


@app.get('/bookmarks/{id}/edit/{book_id}', response_class=HTMLResponse)
async def edit_bookmark_form(request: Request, id: str, book_id: str):
    return templates.TemplateResponse(
        request=request,
        name="edit_book.html",
        context={"id": id, "book": {"id": book_id, "title": "Kane & Able", "current_page": 100, "total_pages": 200}})


@app.post('/bookmarks/{id}/edit/{book_id}', response_class=RedirectResponse)
async def edit_bookmark(request: Request, id: str):
    return RedirectResponse(url=f'/bookmarks/{id}', status_code=status.HTTP_303_SEE_OTHER)
