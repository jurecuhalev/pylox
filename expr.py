from abc import ABC, abstractmethod
from typing import Any, Optional

from tokens import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
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


class Variable(Expr):
    name: Token = None

    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)


class Assign(Expr):
    name: Token = None
    value: Expr = None

    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)


class Logical(Expr):
    left: Optional[Expr] = None
    operator: Optional[Token] = None
    right: Optional[Expr] = None

    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)
