from parser.grammar import Grammar, GrammarToken
from .regex_core import RegexToken

regex_special_tokens = ['?', '+', '*', '^',
                        '$', '[', ']', '(', ')', '{', '}', '.', '|', '-']


class RegexGrammar():
    def __init__(self) -> None:
        self.grammar = self.__get_grammar()

    def __get_grammar(self) -> Grammar:
        g = Grammar()

        g.add_main('S')

        g.add_production('S', ['E'])
        g.add_production('E', ['A | E', 'A'])
        g.add_production('A', ['F A', 'F'])
        g.add_production('F', ['[ G ] I', 'H I'])
        g.add_production(
            'I', ['?', '+', '*',  ''])
        g.add_production('H', ['ch', '( E )', '.'])
        g.add_production('G', ['^ J', 'J'])
        g.add_production('J', ['K J', 'K'])
        g.add_production('K', ['ch', 'ch - ch'])

        return g

    def regex_to_grammar(self, token: RegexToken) -> GrammarToken:
        if token.is_special:
            return [t for t in self.grammar.terminals if t.value == token.value][0]

        return [t for t in self.grammar.terminals if t.value == 'ch'][0]
