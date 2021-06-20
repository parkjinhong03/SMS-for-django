from rest_framework.views import exception_handler

class CustomHttpException(Exception):
    """base exception to customize http error which contains status and code inform"""

    def __init__(self, status: int, code: int):
        self.status, self.code = status, code

    def get_message(self) -> Any:
        raise NotImplementedError


class UnexpectedValidateError(CustomHttpException):
    """represent exception about unexpected validate error inheriting CustomHttpException"""

    def __init__(self, invalid_field: str, validate_errors: Dict[str, List[ErrorDetail]],
                 status: int = HTTP_500_INTERNAL_SERVER_ERROR, code: int = 0):
        super(UnexpectedValidateError, self).__init__(status, code)
        self.invalid_field, self.validate_errors = invalid_field, validate_errors

    def get_message(self) -> Any:
        return {
            'detail': f'unexpected validate error of {self.invalid_field}',
            **self.validate_errors
        }


class DependencyNotImplementedError(Exception):
    """dependency not implemented error which can be raise when DI occurs"""

    def __init__(self, dependency, interface):
        self.dependency = dependency
        self.interface = interface

    def __str__(self):
        return f'dependency not implemented! dependency: {type(self.dependency)}, interface: {self.interface}'
