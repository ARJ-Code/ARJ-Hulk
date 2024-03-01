from .grammar import Grammar, GrammarToken, EOF
from .automatonLR import AutomatonLR, Action
from typing import List
from .parse_out import ParseResult


class Parser:
    def __init__(self, grammar: Grammar, automatonLR: AutomatonLR) -> None:
        self.grammar: Grammar = grammar
        self.aut: AutomatonLR = automatonLR

    def parse(self, tokens: List[GrammarToken]) -> ParseResult:
        tokens.append(EOF())
        productions_result: List[GrammarToken] = []

        index: int = 0
        stack_tokens: List[GrammarToken] = []

        while True:
            action, ind = self.aut.action(
                stack_tokens, tokens[index])

            if action == Action.SHIFT:
                self.shift_action(stack_tokens, tokens[index])
                index += 1

            if action == Action.REDUCE:
                self.reduce_action(stack_tokens, ind, productions_result)

            if action == Action.ERROR:
                return ParseResult(error=index)

            if action == Action.ACCEPT:
                productions_result.reverse()
                return ParseResult(derivations=productions_result)

    def shift_action(self, stack_tokens: List[GrammarToken], input: GrammarToken):
        stack_tokens.append(input)

    def reduce_action(self, stack_tokens: List[GrammarToken], ind: int, productions_result: List[GrammarToken]):
        for production in self.grammar.productions:
            if production.ind == ind:
                productions_result.append(production)

                for _ in range(len(production.body)):
                    stack_tokens.pop()
                stack_tokens.append(production.head)
