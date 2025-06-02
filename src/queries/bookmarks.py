from datetime import datetime, timezone
from tortoise import exceptions

from src.models import Bookmark


async def get_bookmark(id: str) -> Bookmark | None:
    try:
        return await Bookmark.get(id=id)
    except exceptions.DoesNotExist:
        return None


async def update_last_read(bookmark_id: str) -> Bookmark:
    bookmark = await get_bookmark(bookmark_id)

    if not bookmark:
        return None

    today = datetime.now(timezone.utc)

    await bookmark.compute_and_update_streak_length()

    bookmark.last_read_at = today

    await bookmark.save(update_fields=["last_read_at",])

    return bookmark
