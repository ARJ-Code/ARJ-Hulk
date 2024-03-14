from typing import Tuple, List
from .automaton import Automaton
import json

IGNORE: str = 'IGNORE'


class LexerToken:
    def __init__(self, row: int, col: int, value: str, token_type: str) -> None:
        self.value: str = value
        self.row: int = row
        self.col: int = col
        self.type: str = token_type

    def __eq__(self, __value: object) -> bool:
        return self.type == __value.type


class LexerError:
    def __init__(self, msg: str, row: int, col: int) -> None:
        self.msg = msg
        self.row = row
        self.col = col


class LexerResult:
    def __init__(self, tokens: List[LexerToken] = [], error: LexerError | None = None) -> None:
        self.ok: bool = error is None
        self.tokens: List[LexerToken] = tokens
        self.error: LexerError | None = error


class Lexer:
    def __init__(self) -> None:
        self.ignore_automaton: Automaton | None = None
        self.tokens_automaton: List[List[Tuple[str, Automaton]]] = []

    @staticmethod
    def build(name: str, tokens_automaton: List[Tuple[str, Automaton]], ignore_automaton: Automaton):
        result = [(IGNORE, ignore_automaton.to_dfa().to_json())]

        for t, a in tokens_automaton:
            result.append((t, a.to_dfa().to_json()))

        json.dump(result, open(f'cache/{name}_lexer.json', 'w'))

    def load(self, name: str):
        cache = json.load(open(f'cache/{name}_lexer.json'))
        for t, v in cache:
            a = Automaton()
            a.from_json(v)

            if t == IGNORE:
                self.ignore_automaton = a
                continue

            self.tokens_automaton.append((t, a))

    def match(self, text: str, index: int, automaton: Automaton) -> Tuple[str, bool]:
        current_state = automaton.initial_state
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
        tokens: List[LexerToken] = []

        index = 0
        row = 0
        col = 0

        while index != len(text):
            result: str = ''
            token_type: str | None = None

            ignore = [] if self.ignore_automaton is None else [(
                IGNORE, self.ignore_automaton)]

            for t, a in (self.tokens_automaton+ignore):
                current_result, ok = self.match(text, index, a)

                if ok and len(current_result) > len(result):
                    result = current_result
                    token_type = t

            if len(result) == 0:
                return LexerResult(error=LexerError('Invalid character', row, col))

            for c in result:
                if c == '\n':
                    row += 1
                    col = 0
                else:
                    col += 1
            index += len(result)

            if token_type != IGNORE:
                tokens.append(
                    LexerToken(row, col, result, token_type))

        return LexerResult(tokens)
