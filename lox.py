import click

from token_type import TokenType


class Token:
    token_type: TokenType
    lexeme: str
    literal: dict
    line: int

    def __init__(self, token_type: TokenType, lexeme: str, literal: dict, line: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"


class Scanner:
    source: str
    tokens: list[Token]

    def __init__(self, source: str):
        self.source = source

    def scan_tokens(self) -> list[Token]:
        pass


class Lox:
    had_error = False

    def run_file(self, script):
        with open(script) as f:
            source = f.read()

        self.run(source)
        if self.had_error:
            exit(65)

    def run_prompt(self):
        while True:
            line = input("> ")
            self.run(line)
            self.had_error = False

    def run(self, source: str):
        scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def error(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        print(f"[line {line}] Error {where}: message")


@click.command()
@click.argument("script", required=False)
def main(script):
    lox = Lox()

    if script:
        lox.run_file(script)
    else:
        lox.run_prompt()


if __name__ == "__main__":
    main()
