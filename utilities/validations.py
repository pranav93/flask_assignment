import functools
import http

from flask import current_app
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
                current_app.logger.exception('error occurred')
                abort(http.HTTPStatus.BAD_REQUEST, message=re.message, status='error')
            except ResourceDoesNotExist as re:
                current_app.logger.exception('error occurred')
                abort(http.HTTPStatus.NOT_FOUND, message=re.message, status='error')
            except IntegrityError as ie:
                current_app.logger.exception('error occurred')
                abort(http.HTTPStatus.BAD_REQUEST, message=repr(ie), status='error')
            except Exception as e:
                current_app.logger.exception('error occurred')
                abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, message=repr(e), status='error')
        return wrapper
    return wrapped
