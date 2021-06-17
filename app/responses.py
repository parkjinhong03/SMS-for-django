from collections import abc
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class Response(Response):
    """add status, code, msg values which are received from kwarg to data dict"""

    def __init__(self, data: any = None, status: int = HTTP_200_OK, code: int = 0, msg: str = '', *args, **kwargs):
        data = {} if data is None else data
        if isinstance(data, abc.MutableMapping):
            data['status'] = status
            data['code'] = code
            data['message'] = msg
        super(Response, self).__init__(data=data, status=status, *args, **kwargs)
