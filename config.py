import json

with open("config.json", "r") as f:
    _cfg = json.load(f)

USER_ROLE_CACHE_SIZE: int = _cfg["user_role_cache_size"]