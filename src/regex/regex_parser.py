from compiler_tools.grammar import Grammar, GrammarToken
from compiler_tools.parser import Parser
from compiler_tools.parser_out import ParseResult
from compiler_tools.automatonSLR1 import AutomatonSLR1
from compiler_tools.tableLR import TableLR
from typing import List


class RegexParser():
    def __init__(self, g: Grammar) -> None:
        self.grammar: Grammar = g

    def build(self) -> bool:
        a = AutomatonSLR1('regex', self.grammar)
        return a.ok

    def parse(self, l: List[GrammarToken]) -> ParseResult:
        t = TableLR(self.grammar)
        t.load('regex')
        return Parser(self.grammar, t).parse(l)
