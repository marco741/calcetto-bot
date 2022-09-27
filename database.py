from dataclasses import dataclass, field
import redis
import pickle
import config


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
        self._db = redis.from_url(config.REDIS_URL)
        self.init_redis()

    def init_redis(self):
        if not self._db.exists("init_redis"):
            self.where = ""
            self.when = ""
            self.backup = {"where": "", "when": "", "users": []}
            self._db.delete("users")
            self._db.set("backup", pickle.dumps({"where": "", "when": "", "users": []}))
            self._db.set("init_redis", "1")

    @property
    def where(self):
        return self._db.get("where").decode()

    @where.setter
    def where(self, value):
        self._db.set("where", value)

    @property
    def when(self):
        return self._db.get("when").decode()

    @when.setter
    def when(self, value):
        self._db.set("when", value)

    @property
    def backup(self):
        return pickle.loads(self._db.get("backup"))

    @backup.setter
    def backup(self, value):
        self._db.set("backup", pickle.dumps(value))

    def update_user(self, user: User):
        self._db.hset("users", user.user_id, pickle.dumps(user))

    def create_user(self, user_id, username):
        user = User(user_id, username)
        self.update_user(user)

    def delete_user(self, user_id):
        self._db.hdel("users", user_id)

    def is_created(self, user_id) -> bool:
        return self._db.hexists("users", user_id)

    def get_user(self, user_id) -> User:
        return pickle.loads(self._db.hget("users", user_id))

    def get_users(self) -> list[User]:
        return list(map(pickle.loads, self._db.hvals("users")))

    def get_other_users(self, user_id) -> list[User]:
        return [user for user in self.get_users() if user.user_id != user_id]

    def get_players(self) -> list[User]:
        return [user for user in self.get_users() if user.wantstoplay]

    def is_player(self, user_id) -> bool:
        return self.get_user(user_id).wantstoplay

    def set_player(self, user_id, wantstoplay=True):
        user = self.get_user(user_id)
        user.wantstoplay = wantstoplay
        self.update_user(user)

    def reset(self):
        self.backup = {"where": self.where, "when": self.when, "users": self.get_players()}
        self.where = ""
        self.when = ""
        for user in self.get_users():
            user.reset()
            self.update_user(user)
