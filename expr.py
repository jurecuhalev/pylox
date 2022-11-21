from abc import ABC

from tokens import Token


class Expr:
    def accept(self, visitor):
        func = getattr(visitor, f"visit{self.__class__.__name__}")
        return func()


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression


class Literal(Expr):
    def __int__(self, value: any):
        self.value = value


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right
