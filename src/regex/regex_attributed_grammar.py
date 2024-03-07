from parser.parser_out import DerivationTree
from typing import List, Callable
from .regex_ast import *
from .regex_core import RegexToken, RegexResult


class RegexAttributedGrammar():
    def __init__(self) -> None:
        self.non_terminals: List[RegexToken] = []

        # g.add_main('S')

        # g.add_production('S', ['E'])
        # g.add_production('E', ['A | E', 'A'])
        # g.add_production('A', ['F A', 'F'])
        # g.add_production('F', ['[ G ] I', 'H I'])
        # g.add_production(
        #     'I', ['?', '+', '*', '{ ch }', '{ ch , ch }', '{ , ch }', '{ ch , }', ''])
        # g.add_production('H', ['ch', '( E )', '.'])
        # g.add_production('G', ['^ J', 'J'])
        # g.add_production('J', ['K J', 'K'])
        # g.add_production('K', ['ch', 'ch - ch'])

    def to_ast(self, derivation_tree: DerivationTree, non_terminals: List[RegexToken]) -> RegexResult[RegexAst]:
        self.non_terminals = non_terminals
        self.non_terminals.reverse()

        return self.__inherited_attribute(derivation_tree)

    def __terminal(self) -> str:
        t = self.non_terminals[-1].value
        self.non_terminals.pop()

        return t

    def __binary(self, node: DerivationTree, binary_function: Callable[[RegexAst, RegexAst], RegexAst], op: bool = False) -> RegexResult[RegexAst]:

        left = self.__inherited_attribute(node.children[0])
        if op:
            self.__terminal()
        right = self.__inherited_attribute(node.children[2 if op else 1])

        if not left.ok:
            return left
        if not right.ok:
            return right

        return RegexResult[RegexAst](binary_function(left.value, right.value))

    def __inherited_attribute(self, node: DerivationTree) -> RegexResult[RegexAst]:
        production_ind = node.production_ind
   
        if production_ind == 0 or production_ind == 2 or production_ind == 4 or production_ind == 19 or production_ind == 21:
            return self.__inherited_attribute(node.children[0])

        if production_ind == 1:
            return self.__binary(node, lambda x, y: RegexOr(x, y), True)

        if production_ind == 3:
            return self.__binary(node, lambda x, y: RegexConcat(x, y))

        if production_ind == 5:
            self.__terminal()
            param = self.__inherited_attribute(node.children[1])
            self.__terminal()

            if not param.ok:
                return param

            return self.__synthesized_attribute(node.children[3], [param.value])

        if production_ind == 6:
            param = self.__inherited_attribute(node.children[0])

            if not param.ok:
                return param

            return self.__synthesized_attribute(node.children[1], [param.value])

        if production_ind == 15 or production_ind == 22:
            return RegexResult[RegexAst](RegexChar(self.__terminal()))

        if production_ind == 16:
            self.__terminal()
            result = self.__inherited_attribute(node.children[1])
            self.__terminal()

            return result

        if production_ind == 17:
            self.__terminal()

            return RegexResult[RegexAst](RegexAnyChar())

        if production_ind == 18:
            self.__terminal()

            result = self.__inherited_attribute(node.children[1])
            if not result.ok:
                return result

            return RegexResult[RegexAst](RegexNot(result.value))

        if production_ind == 20:
            return self.__binary(node, lambda x, y: RegexOr(x, y))

        if production_ind == 23:
            x = self.__terminal()
            self.__terminal()
            y = self.__terminal()

            return RegexResult[RegexAst](RegexRank(x, y))

    def __synthesized_attribute(self, node: DerivationTree, param: List[RegexAst]) -> RegexResult[RegexAst]:
        production_ind = node.production_ind

        if production_ind == 7:
            self.__terminal()
            return RegexResult[RegexAst](RegexQuestion(param[0]))
        if production_ind == 8:
            self.__terminal()
            return RegexResult[RegexAst](RegexOneAndMany(param[0]))
        if production_ind == 9:
            self.__terminal()
            return RegexResult[RegexAst](RegexMany(param[0]))

        # TODO:
        if production_ind == 14:
            return RegexResult[RegexAst](param[0])
