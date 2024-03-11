from compiler_tools.grammar import Grammar, GrammarToken
from .regex_core import RegexToken

regex_special_tokens = ['?', '+', '*', '^',
                        '$', '[', ']', '(', ')', '{', '}', '.', '|', '-']

regex_grammar = Grammar()

regex_grammar.add_main('S')
regex_grammar.add_production('S', ['E'])
regex_grammar.add_production('E', ['A | E', 'A'])
regex_grammar.add_production('A', ['F A', 'F'])
regex_grammar.add_production('F', ['[ G ] I', 'H I'])
regex_grammar.add_production('I', ['?', '+', '*',  ''])
regex_grammar.add_production('H', ['ch', '( E )', '.'])
regex_grammar.add_production('G', ['^ J', 'J'])
regex_grammar.add_production('J', ['K J', 'K'])
regex_grammar.add_production('K', ['ch', 'ch - ch'])


def regex_to_grammar(token: RegexToken) -> GrammarToken:
    if token.is_special:
        return [t for t in regex_grammar.terminals if t.value == token.value][0]

    return [t for t in regex_grammar.terminals if t.value == 'ch'][0]
