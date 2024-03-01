from .grammar import Grammar, GrammarToken, EOF
from .automatonLR import AutomatonLR,Action
from typing import List


class Parser:
    def __init__(self, grammar: Grammar, automatonLR: AutomatonLR) -> None:
        self.grammar: Grammar = grammar
        self.aut: AutomatonLR = automatonLR

    def parse(self, tokens: List[GrammarToken]):
        tokens.append(EOF())

        index: int = 0
        stack_tokens: List[GrammarToken] = []
      
        while True:
            action, ind = self.aut.action(
                stack_tokens, tokens[index])
            
            if action == Action.SHIFT:
                self.shift_action(stack_tokens, tokens[index])
                index+=1
            
            if action == Action.REDUCE:
                self.reduce_action(stack_tokens, ind)

            

    def shift_action(self, stack_tokens: List[GrammarToken], input: GrammarToken):
        stack_tokens.append(input)

    def reduce_action(self, stack_tokens: List[GrammarToken], ind: int):
        for production in self.grammar.productions:
            if production.ind == ind:
                for _ in range(len(production.body)):
                    stack_tokens.pop()
                stack_tokens.append(production.head)
