from abc import ABCMeta


class HashingCodec(metaclass=ABCMeta):
    """interface to hashing_codec dependency using in View initialize"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'encode') and callable(subclass.encode) and
                hasattr(subclass, 'compare_hash') and callable(subclass.compare_hash)) or \
               NotImplemented


class ObjectStorage(metaclass=ABCMeta):
    """interface to object_storage dependency using in View initialize"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'put_object') and callable(subclass.put_object)) or \
               NotImplemented


class JWTCodec(metaclass=ABCMeta):
    """interface to jwt_codec dependency using in View initialize"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'encode') and callable(subclass.encode) and
                hasattr(subclass, 'decode') and callable(subclass.decode)) or \
               NotImplemented
