from compiler_tools.automatonLR import Node
from .grammar import GrammarProduction, GrammarToken, Grammar, EOF
from .tableLR import NodeAction, Action
from .automatonLR import AutomatonLR
from .itemLR import ItemLR
from typing import Dict, List


class AutomatonSLR1(AutomatonLR[ItemLR]):
    def __init__(self, name: str, grammar: Grammar):
        super().__init__(name, grammar)

    def _build_grammar(self):
        self.grammar.calculate_follow()

    def _get_item(self, production: GrammarProduction, index: int) -> ItemLR:
        item = ItemLR(len(self.items), production, index)
        self.items.append(item)

        return item

    def _build_items(self):
        head_to_item: Dict[GrammarToken, List[GrammarToken]] = {}
        production_to_item: Dict[GrammarProduction, List[ItemLR]] = {}

        for t in self.grammar.non_terminals:
            head_to_item[t] = []

        for p in self.grammar.productions:
            production_to_item[p] = []

        for production in self.grammar .productions:
            for i in range(len(production.body) + 1):
                item = self._get_item(production, i)

                head_to_item[production.head].append(item)
                production_to_item[production].append(item)

        for x in self.items:
            if x.index == len(x.production.body) or x.production.body[x.index].is_terminal:
                continue

            for y in head_to_item[x.production.body[x.index]]:
                if y.index == 0:
                    x.add_eof_transition(y)

        for x in self.items:
            if x.index == len(x.production.body):
                continue

            for y in production_to_item[x.production]:
                if y.index == x.index + 1:
                    x.add_transition(x.production.body[x.index], y)

    def _get_item_main(self) -> ItemLR:
        return [
            item for item in self.items if item.production.head == self.grammar.main and item.index == 0][0]

    def _build_reduce(self, node: Node, node_action: NodeAction, result: bool):
        for item in node.items:
            if item.index == len(item.production.body):
                if item.production.head == self.grammar.main:
                    result = result and node_action.add_terminal_action(
                        EOF(), Action.ACCEPT, -1)
                else:
                    for t in self.grammar.follows[item.production.head]:
                        result = result and node_action.add_terminal_action(
                            t, Action.REDUCE, item.production.ind)

            if not result:
                break

        return result
