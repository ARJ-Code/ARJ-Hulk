from parser.grammar import Grammar, GrammarToken
from parser.parser import Parser
from parser.parse_out import ParseResult
from parser.automatonSLR1 import AutomatonSLR1
from typing import List


class RegexParser():
    def __init__(self, g: Grammar) -> None:
        self.grammar: Grammar = g

    def build(self) -> bool:
        a = AutomatonSLR1('regex', self.grammar)
        return a.ok

    def parse(l: List[GrammarToken]) -> ParseResult:
        return Parser('regex').parse(l)
