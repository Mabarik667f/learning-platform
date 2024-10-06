from loguru import logger
from core.config import settings


class MailingCodeUtils:
    def __init__(self, username) -> None:
        self.username = username
        self.redis = settings.REDIS_URI

    def set_code(self, code: str) -> None:
        self.redis.set(self.username, code)

    def check_code(self, code: str) -> bool:
        true_code = self.redis.get(self.username)
        if true_code is not None and true_code == code:
            self.delete_code()
            return True
        return False

    def delete_code(self) -> None:
        self.redis.delete(self.username)
