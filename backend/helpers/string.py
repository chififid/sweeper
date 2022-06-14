def get_safe_string(string: str) -> str:
    return string.lower().strip().replace(" ", "_")
