import bcrypt
from typing import Dict, List

from constants.enums.privileges import Privileges
from helpers.string import get_safe_string
from objects.player import Player


def check_login(login: str, password: str) -> bool:
    safe_login = get_safe_string(login)
    if safe_login not in users:
        return False

    password = password.encode("utf-8")

    return bcrypt.checkpw(password, users[safe_login])


player = Player(
    1,
    "Admin",
    Privileges.PLAYER | Privileges.SUPPORTER,
)

player.generate_password_bcrypt("Admin")

users: Dict[str, bytes] = {player.safe_name: player.password_bcrypt}  # Safe name: password bcrypt


def save_token(token: str) -> None:
    token_response_dict.append(token)


def check_token(token: str) -> bool:
    if token in token_response_dict:
        return True
    return False


token_response_dict: List[str] = []  # Tokens
