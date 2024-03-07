from parser.grammar import Grammar, GrammarToken
from .regex_core import RegexToken

regex_special_tokens = ['?', '+', '*', '^',
                        '$', '[', ']', '(', ')', '{', '}', '.']


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
            'I', ['?', '+', '*', '{ ch }', '{ ch , ch }', '{ , ch }', '{ ch , }', ''])
        g.add_production('H', ['ch', '( E )', '.'])
        g.add_production('G', ['^ J', 'J'])
        g.add_production('J', ['K J', 'K'])
        g.add_production('K', ['ch', 'ch - ch'])

        return g

    def regex_to_grammar(self, token: RegexToken) -> GrammarToken:
        if token.is_special:
            return [t for t in self.grammar.terminals if t.value == token.value][0]

        return [t for t in self.grammar.terminals if t.value == 'ch'][0]

    # def derivation_to_ast(self, derivation_tree: DerivationTree, non_terminals: List[RegexToken], param: RegexAst | None = None) -> RegexAst:
    #     if derivation_tree.production_ind == -1:
    #         node = RegexChar(non_terminals[-1].value)
    #         non_terminals.pop()

    #         return node

    #     children = [derivation_tree(x, non_terminals)
    #                 for x in derivation_tree.children]

    #     rules = [lambda: children[0],
    #              lambda:RegexOr(children[0], children[1]),
    #              lambda:children[0],
    #              lambda: RegexConcat(children[0], children[1]),
    #              lambda:children[0],
    #              lambda:self.derivation_to_ast(
    #                  derivation_tree.children[1], non_terminals, children[0]),
    #              lambda:self.derivation_to_ast(
    #                  derivation_tree.children[1], non_terminals, children[0]),
    #              lambda:RegexQuestion(param),
    #              lambda:RegexOneAndMany(param),
    #              lambda:RegexMany(param),
    #              lambda:children[0],
    #              ]


# class RegexGrammarRules

# class RegexAttributedGrammar():
#     def __init__(self) -> None:
#         self.non_terminals: List[GrammarToken]=[]

#     def __inherited_attribute(self,node:DerivationTree)->RegexAst:
    