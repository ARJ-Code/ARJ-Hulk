from compiler_tools.automatonLR import Node
from .grammar import GrammarProduction, GrammarToken, Grammar, EOF
from .tableLR import NodeAction, Action
from .itemLR import ItemLR1
from .automatonLR import AutomatonLR


class AutomatonLR1(AutomatonLR[ItemLR1]):
    def __init__(self, name: str, grammar: Grammar):
        super().__init__(name, grammar)

    def _build_grammar(self):
        self.grammar.calculate_first()

    def _get_item(self, production: GrammarProduction, index: int, teal: GrammarToken) -> ItemLR1:
        item = ItemLR1(len(self.items), production, index, teal)
        self.items.append(item)

        return item

    def _get_item_main(self) -> ItemLR1:
        return [
            item for item in self.items if item.production.head == self.grammar.main and item.index == 0 and item.teal == EOF()][0]

    def _build_items(self):
        for production in self.grammar.productions:
            for i in range(len(production.body) + 1):
                for t in self.grammar.terminals:
                    self._get_item(production, i, t)

        for x in self.items:
            for y in self.items:
                if x.index == len(x.production.body):
                    continue

                if y.production.head == x.production.body[x.index] and y.index == 0:
                    w = self.grammar.calculate_sentence_first(
                        x.production.body[x.index+1:]+[x.teal])
                    if y.teal in w:
                        x.add_eof_transition(y)

                if y.production == x.production and y.index == x.index + 1 and x.teal == y.teal:
                    x.add_transition(
                        x.production.body[x.index], y)

    def _build_reduce(self, node: Node, node_action: NodeAction, result: bool) -> bool:     
        for item in node.items:
            if item.index == len(item.production.body):
                if item.production.head == self.grammar.main:
                    result = result and node_action.add_terminal_action(
                        EOF(), Action.ACCEPT, -1)

                else:
                    result = result and node_action.add_terminal_action(
                        item.teal, Action.REDUCE, item.production.ind)

        return result
