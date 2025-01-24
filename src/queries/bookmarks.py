from tortoise import exceptions

from src.models import Bookmark


async def get_bookmark(id: str):
    try:
        return await Bookmark.get(id=id)
    except exceptions.DoesNotExist:
        return None
