from tortoise import fields

from src.models.base import BaseModel


class Bookmark(BaseModel):
    status = fields.BooleanField(default=False)
