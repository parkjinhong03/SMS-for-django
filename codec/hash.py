import bcrypt
from _meta.singleton import Singleton


class BcryptHashingCodec(metaclass=Singleton):
    """class that hash password & compare with hashed using bcrypt algorithm"""
    def __init__(self, encoding='utf8'):
        self.encoding = encoding

    def encode(self, password: str, salt: bytes = bcrypt.gensalt(rounds=4)) -> str:
        return bcrypt.hashpw(bytes(password, self.encoding), salt).decode(encoding=self.encoding)

    def compare_hash(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(bytes(password, encoding=self.encoding), bytes(hashed, encoding=self.encoding))
