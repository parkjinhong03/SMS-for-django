from abc import ABCMeta


class JWTCodec(metaclass=ABCMeta):
    """interface to jwt_codec dependency used in view"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'encode') and callable(subclass.encode) and
                hasattr(subclass, 'decode') and callable(subclass.decode)) or \
               NotImplemented


class ElasticsearchAgency(metaclass=ABCMeta):
    """interface to elasticsearch agent dependency used in view"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'search') and callable(subclass.search)) or \
               NotImplemented
