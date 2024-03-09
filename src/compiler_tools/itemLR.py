from typing import Dict, Set
from .grammar import GrammarProduction, GrammarToken, EOF, List


class ItemLR:
    def __init__(self, ind: int, production: GrammarProduction, index: int) -> None:
        self.production: GrammarProduction = production
        self.index: int = index
        self.ind = ind
        self.transitions: Dict[GrammarToken, Set[int]] = {}

    def __eq__(self, other) -> bool:
        self.ind == other.ind

    def __hash__(self) -> int:
        return self.ind

    def __str__(self) -> str:
        return f"{self.production} {self.index}"

    def add_transition(self, token: GrammarToken, item: 'ItemLR'):
        if token not in self.transitions:
            self.transitions[token] = set()

        self.transitions[token].add(item.ind)

    def add_eof_transition(self, item: 'ItemLR'):
        self.add_transition(EOF(), item)

    def get_transitions(self, token: GrammarToken) -> List[int]:
        if token not in self.transitions:
            return []

        return list(self.transitions[token])

    def get_eof_transitions(self) -> List[int]:
        return self.get_transitions(EOF())


class ItemLR1(ItemLR):
    def __init__(self, ind: int, production: GrammarProduction, index: int, teal: GrammarToken) -> None:
        super().__init__(ind, production, index)
        self.teal = teal

    def __str__(self) -> str:
        return f"{self.production} {self.index} {self.teal}"
