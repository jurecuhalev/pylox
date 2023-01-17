from __future__ import annotations


class LoxRuntimeError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message
