import hashlib
import uuid
from dataclasses import dataclass
from typing import Union, Any

import bcrypt

from constants.enums.action import Action
from constants.enums.gamemods import GameMode
from constants.enums.mods import Mods
from constants.enums.privileges import Privileges
from helpers.string import get_safe_string


@dataclass
class Status:  # The current status of a player
    action: Action = Action.IDLE
    info_text: str = ""
    map_md5: str = ""
    mods: Mods = Mods.NOMOD
    mode: GameMode = GameMode.VANILLA_OSU
    map_id: int = 0


@dataclass
class Geolocation:  # The current status of a player
    latitude: float = 0.0
    longitude: float = 0.0
    country_acronym: str = "xx"
    country_numeric: int = 0  # Special country code


class Player:
    __slots__ = (
        "token",
        "id",
        "name",
        "safe_name",  # Equivalent to `name.lower().replace(' ', '_')`.
        "password_bcrypt",
        "privileges",
        "status",
        "geolocation",
        "utc_offset",
        "timezone",
        "silence_end",  # The UNIX timestamp the player's silence will end at.
        "login_time",
    )

    def __init__(
            self,
            id: int,
            name: str,
            privileges: Union[int, Privileges],
            **extras: Any,
    ) -> None:
        if extras.get("token", None):
            self.token = extras.get("token", None)
        else:
            self.token = self.generate_token()

        self.id = id

        self.name = name
        self.safe_name = self.make_safe_str(self.name)

        self.password_bcrypt: bytes = extras.get("password_bcrypt", b"")

        self.privileges = privileges

        self.status = Status()

        action = extras.get("action", False)
        if action:
            self.status.action = action

        info_text = extras.get("info_text", False)
        if info_text:
            self.status.info_text = info_text

        map_md5 = extras.get("map_md5", False)
        if map_md5:
            self.status.map_md5 = map_md5

        mods = extras.get("mods", False)
        if mods:
            self.status.mods = mods

        mode = extras.get("mode", False)
        if mode:
            self.status.mode = mode

        map_id = extras.get("map_id", False)
        if map_id:
            self.status.map_id = map_id

        self.geolocation = Geolocation()

        latitude = extras.get("latitude", False)
        if latitude:
            self.geolocation.latitude = latitude

        longitude = extras.get("longitude", False)
        if longitude:
            self.geolocation.longitude = longitude

        country_acronym = extras.get("country_acronym", False)
        if country_acronym:
            self.geolocation.country_acronym = country_acronym

        country_numeric = extras.get("country_numeric", False)
        if country_numeric:
            self.geolocation.country_numeric = country_numeric

        self.utc_offset: int = extras.get("utc_offset", 0)
        self.timezone: int = 24 + self.utc_offset
        self.silence_end: int = extras.get("silence_end", 0)
        self.login_time: float = extras.get("login_time", 0.0)

    @staticmethod
    def make_safe_str(name: str) -> str:
        return get_safe_string(name)

    @staticmethod
    def generate_token() -> str:  # Generate random token for client reconnection
        return str(uuid.uuid4())

    def generate_password_bcrypt(self, password: str) -> None:
        pw_md5 = hashlib.md5(password.encode()).hexdigest().encode()  # Get password osu client like
        self.password_bcrypt = bcrypt.hashpw(
            pw_md5,
            bcrypt.gensalt()
        )  # Generate hash for this password(it's for future password verifying)
