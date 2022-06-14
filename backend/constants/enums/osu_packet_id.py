from enum import unique, Enum


@unique
class OsuPacketID(Enum):  # It's from kuriso
    CLIENT_SEND_USER_STATUS = 0
    CLIENT_SEND_IRC_MESSAGE = 1
    CLIENT_EXIT = 2
    CLIENT_REQUEST_STATUS_UPDATE = 3
    CLIENT_PONG = 4
    BANCHO_LOGIN_REPLY = 5
    BANCHO_COMMAND_ERROR = 6
    BANCHO_SEND_MESSAGE = 7
    BANCHO_PING = 8
    BANCHO_HANDLE_IRC_CHANGE_USERNAME = 9
    BANCHO_HANDLE_IRC_QUIT = 10
    BANCHO_HANDLE_OSU_UPDATE = 11
    BANCHO_HANDLE_USER_QUIT = 12
    BANCHO_SPECTATOR_JOINED = 13
    BANCHO_SPECTATOR_LEFT = 14
    BANCHO_SPECTATE_FRAMES = 15
    CLIENT_START_SPECTATING = 16
    CLIENT_STOP_SPECTATING = 17
    CLIENT_SPECTATE_FRAMES = 18
    BANCHO_VERSION_UPDATE = 19
    CLIENT_ERRORREPORT = 20
    CLIENT_CANT_SPECTATE = 21
    BANCHO_SPECTATOR_CANT_SPECTATE = 22
    BANCHO_GET_ATTENTION = 23
    BANCHO_ANNOUNCE = 24
    CLIENT_SEND_IRC_MESSAGE_PRIVATE = 25
    BANCHO_MATCH_UPDATE = 26
    BANCHO_MATCH_NEW = 27
    BANCHO_MATCH_DISBAND = 28
    CLIENT_LOBBY_PART = 29
    CLIENT_LOBBY_JOIN = 30
    CLIENT_MATCH_CREATE = 31
    CLIENT_MATCH_JOIN = 32
    CLIENT_MATCH_PART = 33
    BANCHO_MATCH_JOIN_SUCCESS = 36
    BANCHO_MATCH_JOIN_FAIL = 37
    CLIENT_MATCH_CHANGE_SLOT = 38
    CLIENT_MATCH_READY = 39
    CLIENT_MATCHLOCK = 40
    CLIENT_MATCH_CHANGE_SETTINGS = 41
    BANCHO_FELLOW_SPECTATOR_JOINED = 42
    BANCHO_FELLOW_SPECTATOR_LEFT = 43
    CLIENT_MATCH_START = 44
    BANCHO_MATCH_START = 46
    CLIENT_MATCH_SCORE_UPDATE = 47
    BANCHO_MATCH_SCORE_UPDATE = 48
    CLIENT_MATCH_COMPLETE = 49
    BANCHO_MATCH_TRANSFER_HOST = 50
    CLIENT_MATCH_CHANGE_MODS = 51
    CLIENT_MATCH_LOAD_COMPLETE = 52
    BANCHO_MATCH_ALL_PLAYERS_LOADED = 53
    CLIENT_MATCH_NO_BEATMAP = 54
    CLIENT_MATCH_NOT_READY = 55
    CLIENT_MATCH_FAILED = 56
    BANCHO_MATCH_PLAYER_FAILED = 57
    BANCHO_MATCH_COMPLETE = 58
    CLIENT_MATCH_HAS_BEATMAP = 59
    CLIENT_MATCH_SKIP_REQUEST = 60
    BANCHO_MATCH_SKIP = 61
    BANCHO_UNAUTHORISED = 62
    CLIENT_CHANNEL_JOIN = 63
    BANCHO_CHANNEL_JOIN_SUCCESS = 64
    BANCHO_CHANNEL_AVAILABLE = 65
    BANCHO_CHANNEL_REVOKED = 66
    BANCHO_CHANNEL_AVAILABLE_AUTO_JOIN = 67
    CLIENT_BEATMAP_INFO_REQUEST = 68
    BANCHO_BEATMAP_INFO_REPLY = 69
    CLIENT_MATCH_TRANSFER_HOST = 70
    BANCHO_LOGIN_PERMISSIONS = 71
    BANCHO_FRIENDS_LIST = 72
    CLIENT_FRIEND_ADD = 73
    CLIENT_FRIEND_REMOVE = 74
    BANCHO_PROTOCOL_NEGOTIATION = 75
    BANCHO_TITLE_UPDATE = 76
    CLIENT_MATCH_CHANGE_TEAM = 77
    CLIENT_CHANNEL_LEAVE = 78
    CLIENT_RECEIVE_UPDATES = 79
    BANCHO_MONITOR = 80
    BANCHO_MATCH_PLAYER_SKIPPED = 81
    CLIENT_SET_IRC_AWAY_MESSAGE = 82
    BANCHO_USER_PRESENCE = 83
    CLIENT_USER_STATS_REQUEST = 85
    BANCHO_RESTART = 86
    CLIENT_INVITE = 87
    BANCHO_INVITE = 88
    BANCHO_CHANNEL_LISTING_COMPLETE = 89
    CLIENT_MATCH_CHANGE_PASSWORD = 90
    BANCHO_MATCH_CHANGE_PASSWORD = 91
    BANCHO_BAN_INFO = 92
    CLIENT_SPECIAL_MATCH_INFO_REQUEST = 93
    BANCHO_USER_SILENCED = 94
    BANCHO_USER_PRESENCE_SINGLE = 95
    BANCHO_USER_PRESENCE_BUNDLE = 96
    CLIENT_USER_PRESENCE_REQUEST = 97
    CLIENT_USER_PRESENCE_REQUEST_ALL = 98
    CLIENT_USER_TOGGLE_BLOCK_NON_FRIEND_PM = 99
    BANCHO_USER_PM_BLOCKED = 100
    BANCHO_TARGET_IS_SILENCED = 101
    BANCHO_VERSION_UPDATE_FORCED = 102
    BANCHO_SWITCH_SERVER = 103
    BANCHO_ACCOUNT_RESTRICTED = 104
    BANCHO_RTX = 105
    CLIENT_MATCH_ABORT = 106
    BANCHO_SWITCH_TOURNEY_SERVER = 107
    CLIENT_SPECIAL_JOIN_MATCH_CHANNEL = 108
    CLIENT_SPECIAL_LEAVE_MATCH_CHANNEL = 109
