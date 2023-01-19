from abc import abstractmethod
from typing import Any, Optional

from expr import Expr
from tokens import Token


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


class Var(Stmt):
    initializer: Expr = None
    name: Token = None

    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)


class Block(Stmt):
    statements: list = None

    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)


class If(Stmt):
    condition: Optional[Expr] = None
    then_branch: Optional[Stmt] = None
    else_branch: Optional[Stmt] = None

    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)
