import jwt
from typing import Tuple, Dict, Any, List
from _meta.singleton import Singleton


class PyJWTCodec(metaclass=Singleton):
    """jwt codec class that encode & decode token using PyJWT module"""

    def __init__(self, encode_algorithm: str = 'HS256', decode_algorithms: Tuple[str] = ('HS256',)):
        self.encode_algorithm, self.decode_algorithms = encode_algorithm, decode_algorithms

    def encode(self, payload: Dict[str, Any], key: str, encode_algorithm: str = None):
        if encode_algorithm is None:
            encode_algorithm = self.encode_algorithm
        return jwt.encode(payload=payload, key=key, algorithm=encode_algorithm)

    def decode(self, _jwt: str, key: str, decode_algorithm: List[str] = None):
        if decode_algorithm is None:
            decode_algorithm = self.decode_algorithms
        return jwt.decode(jwt=_jwt, key=key, algorithms=decode_algorithm)
