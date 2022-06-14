from fastapi import APIRouter, Query

from constants.enums.ranked_statuses import RankedStatuses
from dbs.beatmaps_db import beatmaps
from helpers.packets import packets
from objects.beatmap import Beatmap


# urls:
# /web/osu-osz2-getscores.php - GET
get_scores_route = APIRouter()


@get_scores_route.get("/web/osu-osz2-getscores.php")
async def osu_get_scores(
        map_md5: str = Query(..., alias="c", min_length=32, max_length=32),
        map_filename: str = Query(..., alias="f"),
):  # Get inf about bitmap
    if map_md5 in beatmaps:
        print(1)
        beatmap = beatmaps[map_md5]
    else:
        print(2)
        beatmap = Beatmap(map_md5, filename=map_filename, status=RankedStatuses.LOVED)
        await beatmap.set_data_from_osu_api(map_md5)
        beatmaps[map_md5] = beatmap

    return packets.get_scores_packet(beatmap)
