from typing import List, Dict, Any
from rest_framework.views import exception_handler
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.exceptions import ErrorDetail
from app.responses import Response


def custom_http_exception_handler(exc, context) -> Response:
    """handling custom exception as well as django standard error response (Ex, CustomHttpException)"""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None and isinstance(exc, CustomHttpException):
        response = Response(exc.status, exc.code, exc.get_message())

    return response


class CustomHttpException(Exception):
    """base exception to customize http error which contains status and code inform"""

    def __init__(self, status: int, code: int):
        self.status, self.code = status, code

    def get_message(self) -> Any:
        raise NotImplementedError


class RequestInvalidError(CustomHttpException):
    """represent exception about request invalid error inheriting CustomHttpException"""

    def __init__(self, validate_errors: Dict[str, List[ErrorDetail]],
                 status: int = HTTP_400_BAD_REQUEST, code: int = 0):
        super(RequestInvalidError, self).__init__(status, code)
        self.validate_errors = validate_errors

    def get_message(self) -> Any:
        return {
            'detail': 'request data is invalid',
            **self.validate_errors,
        }


class UnexpectedValidateError(CustomHttpException):
    """represent exception about unexpected validate error inheriting CustomHttpException"""

    def __init__(self, invalid_field: str, validate_errors: Dict[str, List[ErrorDetail]],
                 status: int = HTTP_500_INTERNAL_SERVER_ERROR, code: int = 0):
        super(UnexpectedValidateError, self).__init__(status, code)
        self.invalid_field, self.validate_errors = invalid_field, validate_errors

    def get_message(self) -> Any:
        return {
            'detail': f'unexpected validate error of {self.invalid_field}',
            **self.validate_errors,
        }


class UnexpectedError(CustomHttpException):
    """represent exception about unexpected error inheriting CustomHttpException"""

    def __init__(self, error: Exception, detail: str = '', status: int = HTTP_500_INTERNAL_SERVER_ERROR, code: int = 0):
        super(UnexpectedError, self).__init__(status, code)
        self.error, self.detail = error, detail

    def get_message(self) -> Any:
        return {
            'detail': f'unexpected error occurs{f" ({self.detail})" if self.detail else ""}',
            'error': str(self.error),
        }


class NotAuthenticatedError(CustomHttpException):
    """represent exception about not authenticated error inheriting CustomHttpException"""

    def __init__(self, detail: str = '', status: int = HTTP_401_UNAUTHORIZED, code: int = 0):
        super(NotAuthenticatedError, self).__init__(status, code)
        self.detail = detail

    def get_message(self) -> Any:
        return f'not authenticated (detail: {self.detail})'


class ForbiddenError(CustomHttpException):
    """represent exception about not authenticated error inheriting CustomHttpException"""

    def __init__(self, detail: str = '', status: int = HTTP_403_FORBIDDEN, code: int = 0):
        super(ForbiddenError, self).__init__(status, code)
        self.detail = detail

    def get_message(self) -> Any:
        return f'forbidden (detail: {self.detail})'


class DependencyNotImplementedError(Exception):
    """dependency not implemented error which can be raise when DI occurs"""

    def __init__(self, dependency, interface):
        self.dependency = dependency
        self.interface = interface

    def __str__(self):
        return f'dependency not implemented! dependency: {type(self.dependency)}, interface: {self.interface}'


def contain_code_to_error_string(detail_errors: Dict[str, List[ErrorDetail]]) -> Dict[str, List[ErrorDetail]]:
    for key, errors in detail_errors.items():
        for i, error in enumerate(errors):
            detail_errors[key][i] = ErrorDetail(f'{error} (code: {error.code})', error.code)
    return detail_errors
