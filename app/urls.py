from functools import wraps

from api import get_board_acronyms, get_post_id, get_reply_id
from flask import abort, current_app


class URLSpace:
    def __init__(self):
        self.board_acronyms = get_board_acronyms()

    def valid_board_acronym(self, val):
        return val in self.board_acronyms

    @staticmethod
    def validate_board(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            board_acronym = kwargs['board_acronym']
            with current_app.app_context():
                if not current_app.url_space.valid_board_acronym(board_acronym):
                    abort(404)
            return fn(*args, **kwargs)

        return wrapper

    @staticmethod
    def validate_post(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            post_id = kwargs['post_id']
            with current_app.app_context():
                if not get_post_id(post_id):
                    abort(404)
            return fn(*args, **kwargs)

        return wrapper

    @staticmethod
    def validate_reply(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            reply_id = kwargs['reply_id']
            with current_app.app_context():
                if not get_reply_id(reply_id):
                    abort(404)
            return fn(*args, **kwargs)

        return wrapper
