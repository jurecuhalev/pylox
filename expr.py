from typing import Any

from tokens import Token


class Expr:
    pass


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value: Any):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)
