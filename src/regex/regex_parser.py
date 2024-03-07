from parser.grammar import Grammar, GrammarToken
from parser.parser import Parser
from parser.parse_out import ParseResult
from parser.automatonSLR1 import AutomatonSLR1
from typing import List


class RegexGrammar():
    def __init__(self) -> None:
        self.grammar: Grammar = self.__get_grammar()

    def __get_grammar(self) -> Grammar:
        g = Grammar()

        g.add_main('S')

        g.add_production('S', ['E'])
        g.add_production('E', ['A | E', 'A'])
        g.add_production('A', ['B C D'])
        g.add_production('B', ['^', ''])
        g.add_production('D', ['$', ''])
        g.add_production('C', ['F C', 'F'])
        g.add_production('F', ['[ G ]', 'H I'])
        g.add_production(
            'I', ['?', '+', '*', '{ ch }', '{ ch , ch }', '{ , ch }', '{ ch , }'])
        g.add_production('H', ['ch', '( E )', '.'])
        g.add_production('G', ['^ J', 'J'])
        g.add_production('J', ['K J', 'K'])
        g.add_production('K', ['ch', 'ch - ch'])

        return g

    def get_non_terminals(self) -> List[GrammarToken]:
        return [t for t in self.grammar.non_terminals]

    def build(self):
        AutomatonSLR1('regex', self.grammar)

    def parse(l: List[GrammarToken]) -> ParseResult:
        return Parser('regex').parse(l)
