import hashlib
import struct
from datetime import datetime
from functools import cached_property
from typing import List

from helpers.string import get_safe_string


class Score:
    __slots__ = (
        "score_movements",
        "beat_map_md5",
        "username",
        "n_300",
        "n_100",
        "n_50",
        "n_geki",
        "n_katu",
        "n_miss",
        "score",
        "max_combo",
        "perfect",
        "mods",
        "mode",
        "play_time",
        "__dict__",
    )

    def __init__(
            self,
            score_movements: bytes,
            score_data: List[str],
    ) -> None:
        self.score_movements = score_movements
        self.beat_map_md5: str = score_data[0]
        self.username: str = get_safe_string(score_data[1])  # TODO: save player model
        self.n_300: int = int(score_data[3])
        self.n_100: int = int(score_data[4])
        self.n_50: int = int(score_data[5])
        self.n_geki: int = int(score_data[6])
        self.n_katu: int = int(score_data[7])
        self.n_miss: int = int(score_data[8])
        self.score: int = int(score_data[9])
        self.max_combo: int = int(score_data[10])
        self.perfect: int = int(score_data[11] == "True")
        self.mods: int = int(score_data[13])
        self.mode: int = int(score_data[15])
        self.play_time: datetime = datetime.now()

    @cached_property
    def md5(self) -> str:
        return hashlib.md5(
            "{}p{}o{}o{}t{}a{}r{}e{}y{}o{}u{}{}{}".format(
                self.n_100 + self.n_300,
                self.n_50,
                self.n_geki,
                self.n_katu,
                self.n_miss,
                self.beat_map_md5,
                self.max_combo,
                str(self.perfect == 1),
                self.username,
                self.score,
                0,  # TODO: rank
                self.mods,
                "True",  # TODO: ??
            ).encode(),
        ).hexdigest()

    def get_byte_data(self) -> bytes:
        return struct.pack(
            "<hhhhhhihBi",
            self.n_300,
            self.n_100,
            self.n_50,
            self.n_geki,
            self.n_katu,
            self.n_miss,
            self.score,
            self.max_combo,
            self.perfect,
            self.mods,
        )
