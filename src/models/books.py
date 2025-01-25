import pytz

from src.models.base import BaseModel
from tortoise import fields


class Book(BaseModel):
    title = fields.CharField(max_length=255)

    current_page = fields.IntField(default=0)
    total_pages = fields.IntField(default=0)

    bookmark = fields.ForeignKeyField('models.Bookmark', related_name='books')

    def last_read_at(self) -> str:
        ist_tz = pytz.timezone('Asia/Kolkata')

        return self.updated_at.astimezone(ist_tz).strftime('%d-%b-%Y %I:%M %p')

    def __str__(self):
        return f"{self.title} ({self.current_page}/{self.total_pages})"
    
    class Meta:
        ordering = ['-updated_at']
    
    class PydanticMeta:
        computed = ['last_read_at',]
