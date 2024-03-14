from .regex_core import RegexResult, RegexToken
from .regex_lexer import lexer
from typing import List
from .regex_ast import RegexAst
from .regex_grammar import regex_grammar
from .regex_parser import regex_parser, regex_to_grammar
from compiler_tools.automaton import Automaton


class Regex():
    def __init__(self, text: str) -> None:
        result = self.__build(text)

        self.error: str = result.error
        self.ok: bool = result.ok
        self.automaton: Automaton | None = None if not result.ok else result.value.automaton

    def match(self, text: str) -> bool:
        if self.automaton is None:
            return False

        return self.automaton.match(text)

    def __build(self, text: str) -> RegexResult[RegexAst]:
        result = self.__lexer(text)
        if not result.ok:
            return RegexResult[RegexResult](error=result.error)

        return self.__parser(result.value)

    def __lexer(self, text) -> RegexResult[List[RegexToken]]:
        return lexer(text)

    def __parser(self, tokens: List[RegexToken]) -> RegexResult[RegexAst]:
        result = regex_parser([regex_to_grammar(t) for t in tokens])

        if not result.ok:
            return RegexResult[RegexAst](error=result.error)

        return RegexResult[RegexAst](regex_grammar.evaluate(result.derivation_tree, tokens))
