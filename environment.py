from exceptions import LoxRuntimeError
from tokens import Token


class Environment:
    def __init__(self):
        self.values = dict()

    def get(self, name: Token):
        if name in self.values.keys():
            return self.values.get(name)

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'")

    def define(self, name: str, value: object):
        self.values.update({name: value})
