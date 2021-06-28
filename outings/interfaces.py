from abc import ABCMeta


class JWTCodec(metaclass=ABCMeta):
    """interface to jwt_codec dependency using in View initialize"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'encode') and callable(subclass.encode) and
                hasattr(subclass, 'decode') and callable(subclass.decode)) or \
               NotImplemented
