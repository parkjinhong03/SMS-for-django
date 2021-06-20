from rest_framework.views import exception_handler

class CustomHttpException(Exception):
    """base exception to customize http error which contains status and code inform"""

    def __init__(self, status: int, code: int):
        self.status, self.code = status, code

    def get_message(self) -> Any:
        raise NotImplementedError

class DependencyNotImplementedError(Exception):
    """dependency not implemented error which can be raise when DI occurs"""

    def __init__(self, dependency, interface):
        self.dependency = dependency
        self.interface = interface

    def __str__(self):
        return f'dependency not implemented! dependency: {type(self.dependency)}, interface: {self.interface}'
