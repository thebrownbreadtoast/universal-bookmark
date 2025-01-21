from src.models.base import BaseModel
from tortoise import fields


class Book(BaseModel):
    title = fields.CharField(max_length=255)

    current_page = fields.IntField(default=0)
    total_pages = fields.IntField(default=0)

    bookmark = fields.ForeignKeyField('models.Bookmark', related_name='books')

    def __str__(self):
        return f"{self.title} ({self.current_page}/{self.total_pages})"
