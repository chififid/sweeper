api_key = ""


def set_api_key(new_var: str) -> None:
    global api_key

    api_key = new_var


def get_api_key() -> str:
    return api_key
