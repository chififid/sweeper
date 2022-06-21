from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from constants.client import CLIENT_BGS


# urls:
# /web/osu-getseasonal.php - GET
# /web/bancho_connect.php - GET
checks_route = APIRouter()


@checks_route.get("/web/osu-getseasonal.php", response_class=PlainTextResponse)
async def osu_get_seasonal():  # Request backgrounds for first client page
    return str(CLIENT_BGS)


@checks_route.get("/web/bancho_connect.php")
async def bancho_connect():  # Just server check
    return b"ru"

