from .tableLR import AutomatonLR,ItemLR,NodeLR,NodeAction
from .grammar import GrammarProduction, GrammarToken
from typing import List,Dict

class ItemLR:
    def __init__(self, production: GrammarProduction, index: int) -> None:
        self.production: GrammarProduction = production
        self.index: int = index


class NodeLR:
    def __init__(self, ind: int) -> None:
        self.ind: int = ind
        self.items: List[ItemLR] = []
        self.transitions: Dict[GrammarToken, 'NodeLR'] = {}

    def add_item(self, item: ItemLR) -> None:
        self.items.append(item)

    def add_transition(self, token: GrammarToken, node: 'NodeLR') -> None:
        self.transitions[token] = node


class AutomatonSLR(AutomatonLR):
    def __init__(self, grammar):
        super(AutomatonSLR, self).__init__(grammar)
        
    def build(self):
        pass