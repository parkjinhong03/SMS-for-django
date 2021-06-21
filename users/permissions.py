from jwt.exceptions import PyJWTError
from django.conf import settings
from rest_framework import permissions
from app.exceptions import UnexpectedError, NotAuthenticatedError, ForbiddenError


class IsAuthenticated(permissions.BasePermission):
    """custom permission that check if token with uuid payload is exist in authorization"""

    def has_permission(self, request, view):
        if (jwt_codec := getattr(view, 'jwt_codec', None)) is None:
            raise UnexpectedError(AttributeError('view doesn\'t have jwt_codec attribute'), detail='in has_permission')

        if (author := request.META.get('HTTP_AUTHORIZATION', None)) is None:
            raise NotAuthenticatedError('authorization is not exist in request META', code=-11)

        try:
            _type, token = author.split(' ')  # raise ValueError if invalid format
            if _type == 'Bearer':
                payload = jwt_codec.decode(token, key=settings.JWT_SECRET_KEY)  # raise PyJWTError if invalid token
                _, _ = payload['uuid'], payload['type']  # raise KeyError if not exist
                request.token_payload = payload
            else:
                raise NotImplementedError  # raise NotImplementedError if unsupported token type
        except ValueError:
            raise NotAuthenticatedError('invalid format of authorization', code=-12)
        except NotImplementedError:
            raise NotAuthenticatedError('unsupported token type', code=-13)
        except PyJWTError as e:
            raise NotAuthenticatedError(f'invalid token in authorization, err: {e}', code=-14)
        except KeyError:
            raise NotAuthenticatedError('invalid payload value in token', code=-15)

        return True


class IsUUIDOwner(permissions.BasePermission):
    """custom permission that check if this token is owner of this request"""

    def has_permission(self, request, view):
        try:
            if request.token_payload['uuid'] == view.kwargs['student_uuid']:
                return True
            raise ForbiddenError(detail='you cannot access with that uuid in token')
        except (AttributeError, KeyError) as e:
            raise UnexpectedError(e, detail=f'error occurs while checking uuid owner permission')
