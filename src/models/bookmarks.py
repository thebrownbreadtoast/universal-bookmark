from datetime import datetime, timezone
from tortoise import fields

from src.models.base import BaseModel


class Bookmark(BaseModel):
    status = fields.BooleanField(default=False)
    last_read_at = fields.DatetimeField(null=True)
    streak_length = fields.IntField(default=0)

    async def compute_and_update_streak_length(self) -> int:
        today = datetime.now(timezone.utc)

        current_streak_length = self.streak_length

        if self.last_read_at:
            days_since_last_read = (today - self.last_read_at).days

            match days_since_last_read:
                case 0:
                    self.streak_length = (self.streak_length or 1)
                case 1:
                    self.streak_length += 1
                case _:
                    self.streak_length = 0
        else:
            self.streak_length = 0

        if current_streak_length != self.streak_length:
            await self.save(update_fields=["streak_length",])

        return self.streak_length
