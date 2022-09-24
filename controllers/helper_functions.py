from flask_jwt_extended import get_jwt_identity
from flask import abort
from contextlib import contextmanager
from main import db


def authenticate_role_only(role):
    """
    Function to manage authentication for user types: user / manager
    :param role: user or manager
    :return: decorated functions
    """
    def inner(func):
        def wrapper(*args, **kwargs):
            if role not in get_jwt_identity():
                return abort(401, description="You do not have permission for this kind of operation.")
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return inner


@contextmanager
def set_no_expire():
    """
    Context manager function to keep session from expire
    :return: None
    """
    session = db.session()
    session.expire_on_commit = False
    try:
        yield
    finally:
        session.expire_on_commit = True

