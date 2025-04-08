from tinydb import TinyDB, Query
from collections import OrderedDict

USER_ROLE_CACHE_SIZE = 20

ROLE_ADMIN = 0b00000010
ROLE_BAN = 0b00000001
ROLE_SUPPORT = 0b00000100
class UserDatabase:
    _db = TinyDB('data_files/users_db.json')
    _cache = OrderedDict()

    @staticmethod
    def _get_user_role(user_tg_id):
        if user_tg_id in UserDatabase._cache:
            UserDatabase._cache.move_to_end(user_tg_id)
            return UserDatabase._cache[user_tg_id]

        User = Query()
        result = UserDatabase._db.get(User.tg_id == user_tg_id)
        if result:
            UserDatabase._cache[user_tg_id] = result['roles']
            if len(UserDatabase._cache) > USER_ROLE_CACHE_SIZE:
                UserDatabase._cache.popitem(last=False)
        return result

    @staticmethod
    def update_role(user_tg_id, add=None, remove=None):
        User = Query()
        user = UserDatabase._db.get(User.tg_id == user_tg_id)
        if user:
            current_roles = user['roles']
            if add is not None:
                current_roles |= add
            if remove is not None:
                current_roles &= ~remove

            UserDatabase._db.update({'roles': current_roles}, User.tg_id == user_tg_id)
            if user_tg_id in UserDatabase._cache:
                UserDatabase._cache[user_tg_id] = current_roles

    @staticmethod
    def get_user(user_tg_id):
        User = Query()
        return UserDatabase._db.get(User.tg_id == user_tg_id)

    @staticmethod
    def add_user(user_data):
        UserDatabase._db.insert(user_data)

    @staticmethod
    def delete_user(user_tg_id):
        User = Query()
        UserDatabase._db.remove(User.tg_id == user_tg_id)
        if user_tg_id in UserDatabase._cache:
            del UserDatabase._cache[user_tg_id]