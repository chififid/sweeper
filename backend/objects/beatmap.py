from datetime import datetime
from typing import Any

from constants.enums.ranked_statuses import RankedStatuses
from helpers.network import osu_api_request

DEFAULT_LAST_UPDATE = datetime(1970, 1, 1)


class Beatmap:
    __slots__ = (
        "md5",
        "id",
        "set_id",
        "artist",
        "title",
        "version",
        "creator",
        "filename",
        "last_update",
        "status",
        "diff",
    )

    def __init__(
            self,
            md5: str,
            **extras: Any,
    ) -> None:
        self.md5 = md5
        self.id: int = extras.get("id", 0)
        self.set_id: int = extras.get("set_id", 0)

        self.artist: str = extras.get("artist", "")
        self.title: str = extras.get("title", "")
        self.version: str = extras.get("version", "")  # Diff name
        self.creator: str = extras.get("creator", "")
        self.filename: str = extras.get("filename", "")

        self.last_update: datetime = DEFAULT_LAST_UPDATE

        self.status: RankedStatuses = RankedStatuses(extras.get("status", RankedStatuses.LOVED))

        self.diff: float = extras.get("diff", 0.0)

    async def set_data_from_osu_api(self, md5: str) -> bool:
        self.md5 = md5
        data = await osu_api_request("beatmaps/lookup", f"checksum={md5}")

        if not data:
            return False

        self.last_update = datetime.now()
        self.id = data["id"]
        self.set_id = data["beatmapset_id"]
        self.artist = data["beatmapset"]["artist"]
        self.title = data["beatmapset"]["title"]
        self.version = data["version"]
        self.creator = data["beatmapset"]["creator"]
        self.diff = data["difficulty_rating"]

        return True
