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

    def match(self, text: str, index: int, r: Regex) -> Tuple[str, bool]:
        current_state = r.automaton.initial_state
        result = ''
        is_final = False

        while True:
            is_final = current_state.is_final

            if index == len(text):
                break

            current_state = current_state.goto(text[index])

            if current_state is None:
                break

            result += text[index]
            index += 1

        return result, len(result) != 0 and is_final

    def run(self, text: str) -> LexerResult:
        tokens: List[HulkToken] = []
        ignore: str = 'IGNORE'

        index = 0
        row = 0
        col = 0

        while index != len(text):
            result: str = ''
            token_type: str | None = None

            for t, r in self.tokens_regex+[(ignore, self.ignore_regex)]:
                current_result, ok = self.match(text, index, r)

                if ok and len(current_result) > len(result):
                    result = current_result
                    token_type = t

            if len(result) == 0:
                return LexerResult(error=ParsingError('Invalid character', row, col))

            for c in result:
                if c == '\n':
                    row += 1
                    col = 0
                else:
                    col += 1
            index += len(result)

            if token_type != ignore:
                tokens.append(
                    HulkToken(row, col, result, token_type))

        return LexerResult(tokens)
