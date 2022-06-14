import aiohttp

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from constants.api import osu_url


# urls:
# /web/osu-getseasonal.php - GET
# /web/bancho_connect.php - GET
checks_route = APIRouter()


@checks_route.get("/web/osu-getseasonal.php", response_class=PlainTextResponse)
async def osu_get_seasonal():  # Request backgrounds for first client page
    async with aiohttp.ClientSession() as session:
        async with session.get(osu_url + "/web/osu-getseasonal.php") as resp:  # Request to bancho server
            response = await resp.text()
            return response


@checks_route.get("/web/bancho_connect.php")
async def bancho_connect():  # Just server check
    return b"ru"
