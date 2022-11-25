from tokens import TokenType, Token

KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


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
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                )
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                )
            case "/":
                if self._match("/"):
                    # A comment goes until the end of the line.
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                # ignore whitespace
                pass
            case "\n":
                self.line += 1
            case '"':
                self._string()
            case _:
                if self._is_digit(char):
                    self._number()
                elif self._is_alpha(char):
                    self._identifier()
                else:
                    self.interpreter.error(self.line, "Unexpected character.")

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def _add_token(self, token_type, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def _peek(self):
        if self._is_at_end():
            return "\0"

        return self.source[self.current]

    def _peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"

        return self.source[self.current + 1]

    def _is_digit(self, char: str):
        return "0" <= char <= "9"

    def _is_alpha(self, char: str):
        return ("a" <= char <= "z") or ("A" <= char <= "Z") or char == "_"

    def _is_alphanumeric(self, char: str):
        return self._is_alpha(char) or self._is_digit(char)

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        if self._is_at_end():
            self.interpreter.error_line(self.line, "Unterminated string.")
            return

        # The closing ".
        self._advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self):
        while self._is_digit(self._peek()):
            self._advance()

        # Look for a fractional part.
        if self._peek() == "." and self._is_digit(self._peek_next()):
            # Consume the "."
            self._advance()

            while self._is_digit(self._peek()):
                self._advance()

        self._add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def _identifier(self):
        while self._is_alphanumeric(self._peek()):
            self._advance()

        text = self.source[self.start + 1 : self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)

        self._add_token(token_type)
