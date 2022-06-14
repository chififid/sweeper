import time
from typing import Optional, Literal
from datetime import datetime, timedelta

from fastapi import Request, Header, APIRouter

from constants.enums.privileges import Privileges
from helpers.auth import check_token, check_login, save_token
from helpers.network import generate_client_response
from helpers.packets import packets
from objects.player import Player

# urls:
# / - POST
login_route = APIRouter()


@login_route.post("/")
async def login_handler(
        request: Request,
        osu_token: Optional[str] = Header(None),  # The client request
        user_agent: Literal["osu!"] = Header(...),  # Request is sent from osu
):  # Login request
    if osu_token:
        # ---
        # --- The client request while re-connect ---
        # ---

        if osu_token == "" or not check_token(osu_token):
            return generate_client_response(packets.user_id_packet(-5))

        # TODO: recognise osu packets

        # Add packets that were not send early(new online player etc.)

        response = bytearray()
        # TODO: add player queue buffer

        return generate_client_response(bytes(response), osu_token)

    # ---
    # --- Login the user ---
    # ---
    start_time = time.time()  # It's for auth speed test

    login_data = (await request.body()).decode().split("\n")

    # Check login data
    if len(login_data) < 3:
        return generate_client_response(packets.user_id_packet(-1))

    username, password, data = (login_data[0], login_data[1], login_data[2].split("|"))

    if not check_login(username, password):
        return generate_client_response(packets.user_id_packet(-1))

    # Check client date
    time_delta = get_time_from_osu_version(data[0])

    if not data[0][1].isdigit() or time_delta.days > 360:
        response = packets.user_id_packet(-2) + packets.notification_packet(
            "Sorry, you use outdated/bad osu!version. Please update your game to join server."
        )
        return generate_client_response(response)

    # Check tourney client
    is_tourney = "tourney" in data[0]

    if is_tourney:
        response = packets.user_id_packet(-1) + packets.notification_packet(
            "Sorry, tourney client isn't supported at the moment."
        )
        return generate_client_response(response)

    # Create player data
    player = Player(
        1,  # TODO
        username,
        Privileges.PLAYER | Privileges.SUPPORTER,  # TODO
    )

    # Create response
    response = packets.user_id_packet(player.id)
    response += packets.protocol_version_packet(19)
    response += packets.privileges_packet(player.privileges)
    response += packets.user_presence_packet(player)
    response += packets.user_stats_packet(player)
    response += packets.friend_list_packet([])  # TODO
    response += packets.silence_end_packet(player.silence_end if player.silence_end > 0 else 0)
    response += packets.notification_packet(
        f'''Welcome to the BEST server! Authorization took: {round((time.time() - start_time) * 1000, 4)}ms'''
    )
    response += packets.channel_listening_end_packet()

    # TODO: online players packet

    save_token(player.token)  # It's for auto client reconnection

    return generate_client_response(
        response,
        player.token,
    )


def get_time_from_osu_version(osu_client_data: str) -> timedelta:
    osu_version_date = osu_client_data[1:9]
    return datetime.now() - datetime(
        int(osu_version_date[:4]),
        int(osu_version_date[4:6]),
        int(osu_version_date[6:8]),
        00,
        00,
    )
