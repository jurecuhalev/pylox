from lox import Token
from token_type import TokenType


class Scanner:
    source: str
    tokens: list[Token] = []
    start = 0
    current = 0
    line = 1

    def __init__(self, source: str, interpreter):
        self.source = source
        self.interpreter = interpreter

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", {}, self.line))
        return self.tokens

    def _scan_token(self):
        char = self._advance()
        match char:
            case '(':
                self._add_token(TokenType.LEFT_PAREN)
            case ')':
                self._add_token(TokenType.RIGHT_PAREN)
            case '{':
                self._add_token(TokenType.LEFT_BRACE)
            case '}':
                self._add_token(TokenType.RIGHT_BRACE)
            case ',':
                self._add_token(TokenType.COMMA)
            case '.':
                self._add_token(TokenType.DOT)
            case '-':
                self._add_token(TokenType.MINUS)
            case '+':
                self._add_token(TokenType.PLUS)
            case ';':
                self._add_token(TokenType.SEMICOLON)
            case '*':
                self._add_token(TokenType.STAR)
            case _:
                self.interpreter.error(self.line, "Unexpected character.")

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _advance(self):
        return self[self.current + 1]

    def _add_token(self, token_type, literal=None):
        text = self.source[self.start: self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
