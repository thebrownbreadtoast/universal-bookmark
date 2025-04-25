from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from src.models import Book, Bookmark, BookLog


Tortoise.init_models(["src.models"], "models")

Bookmark_Pydantic = pydantic_model_creator(Bookmark)
Book_Pydantic = pydantic_model_creator(Book)
BookLog_Pydantic = pydantic_model_creator(BookLog)
