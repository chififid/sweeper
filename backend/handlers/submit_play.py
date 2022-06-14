import random
import struct
from typing import Union
from base64 import b64decode
from py3rijndael import Pkcs7Padding, RijndaelCbc

from fastapi import Request, Form, APIRouter
from starlette.datastructures import UploadFile
from starlette.datastructures import FormData

from constants.paths import REPLAYS_PATH, REPLAYS_CLIENT_PATH
from dbs.beatmaps_db import beatmaps
from helpers.packets import create_packets
from objects.beatmap import Beatmap
from objects.score import Score


# urls:
# /web/osu-submit-modular-selector.php - POST

submit_play_route = APIRouter()


# Local consts
DATETIME_OFFSET = 0x89F7FF5F7B58000  # It's time from 1/1/0001 date to 1/1/1970 date


@submit_play_route.post("/web/osu-submit-modular-selector.php")
async def osu_submit_modular_selector(
        request: Request,
        iv_b64: bytes = Form(..., alias="iv"),
        osu_version: str = Form(..., alias="osuver"),
        client_hash_b64: bytes = Form(..., alias="s"),
):  # Submit scores
    data = await request.form()
    score_id = random.randint(0, 100)

    # Get score data
    score_data_b64, score_movements_file = parse_form_data_score_params(data)
    score_movements = await score_movements_file.read()

    # Save movements
    replay_movements_file = REPLAYS_PATH / f"{score_id}.osr"
    replay_movements_file.write_bytes(score_movements)

    score_data = magic_decrypt(score_data_b64, osu_version, iv_b64).split(":")

    score = Score(
        score_movements,
        score_data,
    )

    # Create replay object!
    replay_data = bytearray()
    replay_data += struct.pack("<Bi", score.mode, 20200207)
    replay_data += create_packets.write_osu_string(score.beat_map_md5)
    replay_data += create_packets.write_osu_string(score.username)
    replay_data += create_packets.write_osu_string(score.md5)
    replay_data += score.get_byte_data()
    replay_data += b"\x00"  # TODO: hp graph

    timestamp = int(score.play_time.timestamp() * 1e7)
    replay_data += struct.pack("<q", timestamp + DATETIME_OFFSET)

    replay_data += struct.pack("<i", len(score_movements))
    replay_data += score_movements

    replay_data += struct.pack("<q", score_id)

    # Generate replay file name
    if score.beat_map_md5 in beatmaps:
        beatmap = beatmaps[score.beat_map_md5]
        beatmap_info = f"{beatmap.title}[{beatmap.id}]"  # TODO: add score user id
    else:
        beatmap_info = f"Unknown beatmap"
    replay_name = f"{beatmap_info} - {score.username}"

    # Save replay
    replay_file = REPLAYS_CLIENT_PATH / f"{replay_name}.osr"
    replay_file.write_bytes(replay_data)  # TODO: take out this code to get score function

    return b"error: no"  # TODO: return beatmap info


def parse_form_data_score_params(
    score_data: FormData,
) -> tuple[bytes, UploadFile]:
    return (
        score_data.getlist("score")[0].encode(),
        score_data.getlist("score")[1]
    )


def magic_decrypt(  # It's from gulag
    s: Union[bytes, str],
    osu_version: str,
    iv_b64: bytes
) -> str:
    aes = RijndaelCbc(
        key=f"osu!-scoreburgr---------{osu_version}".encode(),
        iv=b64decode(iv_b64),
        padding=Pkcs7Padding(32),
        block_size=32,
    )
    return aes.decrypt(b64decode(s)).decode()
