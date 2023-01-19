from __future__ import annotations

import typing
import expr
import stmt
import tokens
from environment import Environment
from exceptions import LoxRuntimeError
from visitor import Visitor
from tokens import TokenType

if typing.TYPE_CHECKING:
    import lox

# noinspection PyShadowingNames
class Interpreter(Visitor):
    def __init__(self, interpreter: lox.Lox):
        self.interpreter = interpreter
        self.environment = Environment()

    def interpret(self, statements: list[stmt.Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as error:
            self.interpreter.runtime_error(error)

    def visit_literal_expr(self, expr: expr.Literal):
        return expr.value

    def visit_grouping_expr(self, expr: expr.Grouping):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: expr.Unary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)

    def visit_variable_expr(self, expr: expr.Variable):
        return self.environment.get(expr.name.lexeme)

    def check_number_operand(self, operator: tokens.Token, operand):
        if isinstance(operand, float):
            return

        raise LoxRuntimeError(operator, "Operands must be numbers.")

    def check_number_operands(self, operator: tokens.Token, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return

        raise LoxRuntimeError(operator, "Operand must be a number.")

    def is_truthy(self, object: object):
        if object is None:
            return False

        if isinstance(object, bool):
            return object

        return True

    def is_equal(self, a: object, b: object):
        if a is None and b is None:
            return True

        if a is None:
            return False

        return a == b

    def stringify(self, _object):
        if _object is None:
            return "nil"

        return str(_object)

    def evaluate(self, expr: expr.Expr):
        return expr.accept(self)

    def execute(self, stmt: stmt.Stmt):
        stmt.accept(self)

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_block_stmt(self, stmt: stmt.Block):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_expression_stmt(self, stmt: stmt.Stmt):
        self.evaluate(stmt.expression)

    def visit_print_stmt(self, stmt: stmt.Stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_var_stmt(self, stmt: stmt.Var):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_assign_expr(self, expr: expr.Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_binary_expr(self, expr: expr.Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left <= right
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - right
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right

                if isinstance(left, str) and isinstance(right, str):
                    return left + right

                raise LoxRuntimeError(
                    expr.operator,
                    "Operands must be two numbers or two strings.",
                )
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return left / right
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return left * right
