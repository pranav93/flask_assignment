import functools
import http

from flask_restful import abort
from sqlalchemy.exc import IntegrityError

from utilities.exceptions import ResourceExists, ResourceDoesNotExist


def handle_exceptions():
    def wrapped(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except ResourceExists as re:
                abort(http.HTTPStatus.BAD_REQUEST, message=re.message)
            except ResourceDoesNotExist as re:
                abort(http.HTTPStatus.NOT_FOUND, message=re.message)
            except IntegrityError as ie:
                abort(http.HTTPStatus.BAD_REQUEST, message=repr(ie))
            except Exception as e:
                abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, message=repr(e))
        return wrapper
    return wrapped
