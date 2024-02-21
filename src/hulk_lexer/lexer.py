from typing import Tuple, List, Callable
from hulk_core.token import TokenType, Token
from hulk_core.error import ParsingError
from .analyzer import Analyzer, AnalyzerResult


class LexerResult:
    def __init__(self, tokens: List[Token], error: ParsingError | None = None) -> None:
        self.ok = error is None
        self.tokens = tokens
        self.error = error


class Lexer:
    def __init__(self, *token_analyzers: Tuple[TokenType], ignore_analyzer: Analyzer) -> None:
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
            result: AnalyzerResult | None = None
            token_type: TokenType | None = None

            for t, a in self.token_analyzers+[(None, self.ignore_analyzer)]:
                if a.match(index, text):
                    current_result = a.run(index, row, col, text)

                    if current_result.ok:
                        if result is None or result.index < current_result.index:
                            result = current_result
                            token_type = t
                    else:
                        return LexerResult([], result.error)

            if result is None:
                return LexerResult([], ParsingError('Invalid character', row, col))

            row = result.row
            col = result.col
            index = result.index

            if not result.empty and token_type is not None:
                tokens.append(
                    Token(result.row, result.col, result.token, token_type))

        return LexerResult(tokens)
