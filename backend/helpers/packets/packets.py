from typing import List

from constants.enums.osu_packet_id import OsuPacketID
from constants.enums.osu_types import OsuTypes
from helpers.packets.create_packets import create_packet
from objects.beatmap import Beatmap
from objects.player import Player


def notification_packet(message: str) -> bytes:
    # Id responses:
    # -1: authentication failed
    # -2: old client
    # -3: banned
    # -4: banned
    # -5: error occurred
    # -6: needs supporter
    # -7: password reset
    # -8: requires verification
    # ??: valid id

    return create_packet(
        OsuPacketID.BANCHO_ANNOUNCE,
        (message, OsuTypes.STRING)
    )


def user_id_packet(user_id: int) -> bytes:
    return create_packet(
        OsuPacketID.BANCHO_LOGIN_REPLY,
        (user_id, OsuTypes.INT32)
    )


def protocol_version_packet(p_version: int) -> bytes:
    return create_packet(
        OsuPacketID.BANCHO_PROTOCOL_NEGOTIATION,
        (p_version, OsuTypes.INT32),
    )


def privileges_packet(privs: int) -> bytes:
    return create_packet(
        OsuPacketID.BANCHO_LOGIN_PERMISSIONS,
        (privs, OsuTypes.INT32),
    )


def user_presence_packet(player: Player) -> bytes:
    return create_packet(
        OsuPacketID.BANCHO_USER_PRESENCE,
        (player.id, OsuTypes.INT32),  # Id
        (player.name, OsuTypes.STRING),  # Username
        (player.timezone, OsuTypes.U_INT8),  # Timezone
        (player.geolocation.country_numeric, OsuTypes.U_INT8),  # Country
        (player.privileges, OsuTypes.U_INT8),  # Bancho privileges
        (player.geolocation.latitude, OsuTypes.FLOAT64),  # Latitude
        (player.geolocation.longitude, OsuTypes.FLOAT64),  # Longitude
        (333, OsuTypes.INT32),  # TODO: leaderboard rank
    )


def user_stats_packet(player: Player) -> bytes:
    return create_packet(
        OsuPacketID.BANCHO_HANDLE_OSU_UPDATE,
        (player.id, OsuTypes.INT32),  # Leaderboard id
        (player.status.action, OsuTypes.U_INT8),  # Action value
        (player.status.info_text, OsuTypes.STRING),  # Action text
        (player.status.map_md5, OsuTypes.STRING),  # Mods map md5
        (player.status.mods.value, OsuTypes.INT32),  # Mods id
        (player.status.mode.value, OsuTypes.U_INT8),  # Mode id
        (player.status.map_id, OsuTypes.INT32),  # Map id
        (1000, OsuTypes.INT64),  # TODO: Ranked score
        (1, OsuTypes.FLOAT32),  # TODO: Accuracy
        (1000, OsuTypes.INT32),  # TODO: Total plays
        (1000, OsuTypes.U_INT64),  # TODO: Total score
        (333, OsuTypes.INT32),  # TODO: Leaderboard rank
        (10000, OsuTypes.INT16),  # TODO: Pp
    )


def friend_list_packet(friend_list: List[int]) -> bytes:
    return create_packet(
        OsuPacketID.BANCHO_FRIENDS_LIST,
        (friend_list, OsuTypes.I32_LIST),
    )


def silence_end_packet(silence_time: int) -> bytes:
    return create_packet(
        OsuPacketID.BANCHO_BAN_INFO,
        (silence_time, OsuTypes.U_INT32),
    )


def channel_listening_end_packet() -> bytes:
    return create_packet(
        OsuPacketID.BANCHO_CHANNEL_LISTING_COMPLETE,
    )


def get_scores_packet(beatmap: Beatmap) -> bytes:
    data = "{}|false|{}|{}|{}\n0\n{}\n{}\n".format(
        beatmap.status,
        beatmap.id,
        beatmap.set_id,
        0,  # TODO: count scores
        beatmap.title,
        beatmap.diff,
    )

    print(data)

    return data.encode()
