import expr
from expr import Visitor
from tokens import TokenType
import numbers


# noinspection PyShadowingNames
class Interpreter(Visitor):
    def visit_literal_expr(self, expr: expr.Literal):
        return expr.value

    def visit_grouping_expr(self, expr: expr.Grouping):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: expr.Unary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)

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

    def evaluate(self, expr: expr.Expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: expr.Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.GREATER:
                return left > right
            case TokenType.GREATER_EQUAL:
                return left >= right
            case TokenType.LESS:
                return left < right
            case TokenType.LESS_EQUAL:
                return left <= right
            case TokenType.MINUS:
                return left - right
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.PLUS:
                if type(left) in ['integer', 'float'] and type(right) in ['integer', 'float']:
                    return left + right

                if isinstance(left, str) and isinstance(right, str):
                    return left + right
            case TokenType.SLASH:
                return left / right
            case TokenType.STAR:
                return left * right
