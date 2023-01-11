from abc import abstractmethod
from typing import Any

from expr import Expr


class Stmt:
    expression = None

    @abstractmethod
    def accept(self, expr: Any):
        pass


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)


class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)
