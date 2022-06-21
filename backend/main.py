import asyncio
import json
import os
import aiohttp
import dotenv

from fastapi import FastAPI

from constants.api import osu_url
from dbs.db import set_api_key
from handlers.checks import checks_route
from handlers.get_scores import get_scores_route
from handlers.login import login_route
from handlers.submit_play import submit_play_route

app = FastAPI()
app.include_router(checks_route)
app.include_router(get_scores_route)
app.include_router(login_route)
app.include_router(submit_play_route)

# consts
dotenv.load_dotenv()
OSU_CLIENT_ID = os.getenv("OSU_CLIENT_ID")
OSU_CLIENT_SECRET = os.getenv("OSU_CLIENT_SECRET")


@app.on_event("startup")
async def startup_event():
    asyncio.get_event_loop().create_task(get_osu_api_token_and_sleep())


async def get_osu_api_token_and_sleep():
    while True:
        sleep_time = await get_osu_api_token() 

        # Get new api token before last token expires
        await asyncio.sleep(sleep_time - 30) 


 # Set osu token in db and return expiration time
async def get_osu_api_token() -> int:
    url = "{}/oauth/token".format(osu_url)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    body = {
        "client_id": int(OSU_CLIENT_ID),
        "client_secret": OSU_CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "public"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=json.dumps(body), \
                                headers=headers) as resp:
            response = json.loads(await resp.text())
            set_api_key(response["access_token"])
            return response["expires_in"]

