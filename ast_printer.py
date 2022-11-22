import expr
from tokens import Token, TokenType


class AstPrinter(expr.Expr):
    def print(self, expr: expr.Expr):
        return expr.accept(self)

    def visit_binary(self, expr: expr.Binary):
        return self._parenthisize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr: expr.Grouping):
        return self._parenthisize("group", expr.expression)

    def visit_literal(self, expr: expr.Literal):
        if not expr.value:
            return "nil"

        return str(expr.value)

    def visit_unary(self, expr: expr.Unary):
        return self._parenthisize(expr.operator.lexeme, expr.right)

    def _parenthisize(self, name: str, *args):
        builder = f"({name}"
        for _expr in args:
            builder += f" {_expr.accept(self)}"
        builder += ")"

        return builder


if __name__ == '__main__':
    expression = expr.Binary(
        expr.Unary(
            Token(TokenType.MINUS, "-", None, 1),
            expr.Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        expr.Grouping(
            expr.Literal(45.67)
        )
    )
    print(AstPrinter().print(expression))
