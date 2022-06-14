import json
import aiohttp
from typing import Optional, Dict, Any

from fastapi import Response

from constants.api import osu_url
from constants.http_headers import client_headers
from dbs.db import get_api_key


def generate_headers_with_token(token: Optional[str] = None):
    headers = client_headers

    if token:
        headers["cho-token"] = token

    return headers


def generate_client_response(content: bytes, token: Optional[str] = None):
    return Response(
        content=bytes(content),
        headers=generate_headers_with_token(token)
    )


async def osu_api_request(
    request: str,
    params: str,
) -> Optional[Dict[str, Any]]:
    url = "{}/api/v2/{}?{}".format(osu_url, request, params)
    headers = {
        "Authorization": f"Bearer {get_api_key()}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            response = json.loads(await resp.text())

    if not ("authentication" in response or "error" in response):
        return response
