import bcrypt


class BcryptHashingCodec:
    """class that hash password & compare with hashed using bcrypt algorithm"""

    def hashpw(self, password: str, salt: bytes = bcrypt.gensalt(rounds=4)) -> str:
        return bcrypt.hashpw(bytes(password, encoding='utf8'), salt).decode(encoding='utf8')

    def checkpw(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(bytes(password, encoding='utf8'), bytes(hashed, encoding='utf8'))
