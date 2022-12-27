from __future__ import annotations

import typing
import expr
import tokens
from expr import Visitor
from tokens import TokenType

if typing.TYPE_CHECKING:
    import lox


class LoxRuntimeError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message


# todo: LoxRuntimeError


# noinspection PyShadowingNames
class Interpreter(Visitor):
    def __init__(self, interpreter: lox.Lox):
        self.interpreter = interpreter

    def interpret(self, expression: expr.Expr):
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except LoxRuntimeError as error:
            self.interpreter.runtime_error(error)

    def visit_literal(self, expr: expr.Literal):
        return expr.value

    def visit_grouping(self, expr: expr.Grouping):
        return self.evaluate(expr.expression)

    def visit_unary(self, expr: expr.Unary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)

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

    def visit_binary(self, expr: expr.Binary):
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
