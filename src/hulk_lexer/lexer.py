from typing import Tuple, List, Callable
from hulk_core.token import HulkToken
from hulk_core.error import ParsingError
from regex.regex import Regex, RegexResult


class LexerResult:
    def __init__(self, tokens: List[HulkToken] = [], error: ParsingError | None = None) -> None:
        self.ok: bool = error is None
        self.tokens: List[HulkToken] = tokens
        self.error: ParsingError | None = error


class Lexer:
    def __init__(self, *tokens_regex: Tuple[str, Regex], ignore_regex: Regex) -> None:
        if len(tokens_regex) == 1 and isinstance(tokens_regex[0], list):
            self.tokens_regex: List[Tuple[str, Regex]] = tokens_regex[0]
        else:
            self.tokens_regex: List[Tuple[str, Regex]] = list(
                tokens_regex)

        self.ignore_regex: Regex = ignore_regex

    def run(self, text: str) -> LexerResult:
        tokens: List[HulkToken] = []
        ignore: str = 'IGNORE'

        index = 0
        row = 0
        col = 0

        while index != len(text):
            result: RegexResult | None = None
            token_type: str | None = None

            for t, r in self.tokens_regex+[(ignore, self.ignore_regex)]:
                current_result = r.match(text, index)
                if current_result.ok and len(current_result.value) != 0:
                    if result is None or len(current_result.value) > len(result.value):
                        result = current_result
                        token_type = t

            if result is None:
                return LexerResult(error=ParsingError('Invalid character', row, col))

            for c in result.value:
                if c == '\n':
                    row += 1
                    col = 0
                else:
                    col += 1
            index += len(result.value)

            if token_type != ignore:
                tokens.append(
                    HulkToken(row, col, result.value, token_type))

        return LexerResult(tokens)
