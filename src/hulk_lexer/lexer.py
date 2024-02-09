from typing import Tuple, List
from hulk_core.token import TokenType, Token
from hulk_core.error import ParsingError
from .analyzer import Analyzer


class LexerResult:
    def __init__(self, tokens: List[Token], error: ParsingError | None = None) -> None:
        self.ok = error is None
        self.tokens = tokens
        self.error = error


class Lexer:
    def __init__(self, *token_analyzers: Tuple[TokenType, Analyzer], ignore_analyzer: Analyzer) -> None:
        if len(token_analyzers) == 1 and isinstance(token_analyzers[0], list):
            self.token_analyzers: List[Tuple[TokenType,
                                             Analyzer]] = token_analyzers[0]
        else:
            self.token_analyzers: List[Tuple[TokenType, Analyzer]] = list(
                token_analyzers)

        self.ignore_analyzer: Analyzer = ignore_analyzer

    def run(self, text: str) -> LexerResult:
        tokens: List[Token] = []

        index = 0
        row = 0
        col = 0

        while index != len(text):
            match = False

            if self.ignore_analyzer.match(index, text):
                result = self.ignore_analyzer.run(index, row, col, text)

                if result.ok:
                    index = result.index
                    row = result.row
                    col = result.col
                else:
                    return LexerResult([], result.error)
                continue

            for t, a in self.token_analyzers:
                if a.match(index, text):
                    result = a.run(index, row, col, text)

                    if result.ok:
                        if not result.empty:
                            tokens.append(Token(row, col, result.token, t))

                        index = result.index
                        row = result.row
                        col = result.col
                    else:
                        return LexerResult([], result.error)

                    match = True
                    break
            if not match:
                return LexerResult([], ParsingError('Invalid character', row, col))

        return LexerResult(tokens)
