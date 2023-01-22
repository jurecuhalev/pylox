from __future__ import annotations
from typing import Optional

from exceptions import LoxRuntimeError
from tokens import Token


class Environment:
    enclosing: Optional[Environment] = None

    def __init__(self, enclosing=None):
        self.values = dict()
        self.enclosing: Optional[Environment] = enclosing

    def get(self, name: Token):
        if name.lexeme in self.values.keys():
            return self.values.get(name.lexeme)

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'")

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values.keys():
            self.values.update({name.lexeme: value})
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'")

    def define(self, name: str, value: object):
        self.values.update({name: value})
