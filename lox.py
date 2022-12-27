from __future__ import annotations
from typing import Optional
import sys

import click

from ast_printer import AstPrinter
from interpreter import Interpreter

# noinspection PyCompatibility
from parser import Parser
from scanner import Scanner
from tokens import Token, TokenType


class Lox:
    had_error = False
    had_runtime_error = False

    def __init__(self):
        self.interpreter = Interpreter(interpreter=self)

    def run_file(self, script):
        with open(script) as f:
            source = f.read()

        self.run(source)
        if self.had_error:
            exit(65)
        if self.had_runtime_error:
            exit(70)

    def run_prompt(self):
        while True:
            line = input("> ")
            self.run(line)
            self.had_error = False

    def run(self, source: str):
        scanner = Scanner(source, interpreter=self)
        tokens: list[Token] = scanner.scan_tokens()
        parser = Parser(tokens, interpreter=self)
        expression = parser.parse()

        if self.had_error:
            return

        # print(AstPrinter().print(expression))
        self.interpreter.interpret(expression)

    def error(
        self, line: Optional[int] = None, token: Optional[Token] = None, message=""
    ):
        self.had_error = True
        if not token:
            self.report(line, "", message)
        elif token.type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)

    def runtime_error(self, error):
        print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
        self.had_runtime_error = True

    def report(self, line, where, message):
        print(f"[line {line}] Error {where}: {message}")


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
