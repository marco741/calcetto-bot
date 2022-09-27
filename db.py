from dataclasses import dataclass, field


@dataclass
class User:
    user_id: str = field(hash=True)
    username: str = field(compare=False, repr=True)
    wantstoplay: bool = field(default=False, compare=False)

    def reset(self):
        self.wantstoplay = False

    def __repr__(self):
        return self.username


class Database:
    def __init__(self):
        self._db = {}
        self.where = ""
        self.when = ""
        self._backup = {"where": "", "when": "", "users": []}

    def register_user(self, user_id, username) -> User | None:
        old_user = self._db.get(user_id)
        self._db[user_id] = User(user_id, username)
        return old_user

    def is_registered(self, user_id) -> bool:
        return user_id in self._db

    def get_users(self) -> list[User]:
        return [user for user in self._db.values]

    def get_other_users(self, user_id) -> list[User]:
        return [user for user in self._db.values() if user.user_id != user_id]

    def get_players(self) -> list[User]:
        return [user for user in self._db.values() if user.wantstoplay]

    def is_player(self, user_id) -> bool:
        return self._db.get(user_id).wantstoplay

    def set_player(self, user_id, wantstoplay=True):
        self._db.get(user_id).wantstoplay = wantstoplay

    def get_user(self, user_id) -> User:
        return self._db.get(user_id)

    def reset(self):
        self._backup = {"where": self.where, "when": self.when, "users": self._db.values()}
        self.where = ""
        self.when = ""
        for user in self._db.values():
            user.reset()

    def get_backup(self):
        return self._backup
