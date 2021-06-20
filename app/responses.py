from collections import abc
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class Response(Response):
    """add status, code, msg values which are received from kwarg to data dict"""

    def __init__(self, status: int = HTTP_200_OK, code: int = 0, msg: any = '', data: any = None, *args, **kwargs):
        data = {} if data is None else data
        if isinstance(data, abc.MutableMapping):
            data['status'], data['code'], data['message'] = status, code, msg
        super(Response, self).__init__(status=status, data=data, *args, **kwargs)
