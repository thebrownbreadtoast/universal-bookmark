import pytz

from datetime import datetime, timezone
from tortoise import fields

from src.models.base import BaseModel


class Bookmark(BaseModel):
    status = fields.BooleanField(default=False)
    last_read_at = fields.DatetimeField(null=True)
    streak_length = fields.IntField(default=0)

    async def compute_and_update_streak_length(self) -> int:
        local_tz = pytz.timezone('Asia/Kolkata')

        today = local_tz.localize(datetime.now()).date()

        current_streak_length = self.streak_length

        if self.last_read_at:
            last_read_at = self.last_read_at.astimezone(local_tz).date()

            time_delta_since_last_read = (today - last_read_at).days

            if (time_delta_since_last_read == 0):
                self.streak_length = (self.streak_length or 1)
            elif (time_delta_since_last_read == 1):
                self.streak_length += 1
            else:
                self.streak_length = 1
        else:
            self.streak_length = 0

        if current_streak_length != self.streak_length:
            await self.save()

        return self.streak_length

    async def check_and_reset_streak_length(self) -> int:
        local_tz = pytz.timezone('Asia/Kolkata')

        today = local_tz.localize(datetime.now()).date()

        current_streak_length = self.streak_length

        if self.last_read_at:
            last_read_at = self.last_read_at.astimezone(local_tz).date()

            time_delta_since_last_read = (today - last_read_at).days

            if (time_delta_since_last_read > 1):
                self.streak_length = 0
        else:
            self.streak_length = 0

        if current_streak_length != self.streak_length:
            await self.save()

        return self.streak_length
