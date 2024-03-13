from typing import Tuple, List
from hulk_core.token import HulkToken
from hulk_core.error import ParsingError
from regex.regex import Regex
from compiler_tools.automaton import Automaton
import json

IGNORE: str = 'IGNORE'


class LexerResult:
    def __init__(self, tokens: List[HulkToken] = [], error: ParsingError | None = None) -> None:
        self.ok: bool = error is None
        self.tokens: List[HulkToken] = tokens
        self.error: ParsingError | None = error


class Lexer:
    def __init__(self, tokens_regex: List[List[Tuple[str, Regex]]] = [], ignore_regex: Regex = None) -> None:
        self.ignore_regex: Regex | None = ignore_regex
        self.tokens_regex: List[List[Tuple[str, Regex]]] = tokens_regex

    @staticmethod
    def build(name: str, token_regex: List[Tuple[str, Regex]], ignore_regex: Regex):
        result = [(IGNORE, ignore_regex.automaton.to_json())]

        for t, r in token_regex:
            result.append((t, r.automaton.to_json()))

        json.dump(result, open(f'cache/{name}_lexer.json', 'w'))

    def load(self, name: str):
        cache = json.load(open(f'cache/{name}_lexer.json'))
        for t, v in cache:
            a = Automaton()
            a.from_json(v)

            if t == IGNORE:
                self.ignore_regex = Regex(automaton=a)
                continue

            self.tokens_regex.append((t, Regex(automaton=a)))

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

        index = 0
        row = 0
        col = 0

        while index != len(text):
            result: str = ''
            token_type: str | None = None

            ignore = [] if self.ignore_regex is None else [(
                IGNORE, self.ignore_regex)]

            for t, r in (self.tokens_regex+ignore):
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

            if token_type != IGNORE:
                tokens.append(
                    HulkToken(row, col, result, token_type))

        return LexerResult(tokens)
