from .grammar import GrammarProduction, GrammarToken, Grammar, EOF
from typing import List, Dict, Set
from .tableLR import TableLR, NodeAction, Action


class ItemLR:
    def __init__(self, ind: int, production: GrammarProduction, index: int) -> None:
        self.production: GrammarProduction = production
        self.index: int = index
        self.ind = ind


class NodeLR:
    def __init__(self, ind: int) -> None:
        self.ind: int = ind
        self.items: Set[ItemLR] = set()
        self.transitions: Dict[GrammarToken, int] = {}

    def add_item(self, item: ItemLR) -> None:
        self.items.add(item)

    def add_transition(self, token: GrammarToken, node: 'NodeLR') -> None:
        self.transitions[token] = node.ind


class AutomatonSLR:
    def __init__(self, name: str, grammar: Grammar):
        self.grammar: Grammar = grammar
        self.items: List[ItemLR] = []
        self.nodes: List[NodeLR] = []
        self.item_to_node: List[NodeLR | None] = []

        self.build_items()
        self.build_nodes()
        self.build_transitions()
        self.build_table(name)

    def build_items(self):
        for production in self.grammar .productions:
            for i in range(len(production.body) + 1):
                self.items.append(ItemLR(len(self.items), production, i))

        self.item_to_node = [None for _ in self.items]

    def build_nodes(self):
        for item in self.items:
            node = self.item_to_node[item.ind]

            if node is None:
                node = NodeLR(len(self.nodes))
                node.add_item(item)
                self.nodes.append(node)
                self.item_to_node[item.ind] = node

            if item.index == len(item.production.body):
                continue

            for item_c in self.items:
                if item_c.production.head == item.production.body[item.index] and item_c.index == 0:
                    self.item_to_node[item_c.ind] = node
                    node.add_item(item_c)

    def build_transitions(self):
        for item in self.items:
            node = self.item_to_node[item.ind]

            if item.index == len(item.production.body):
                continue

            for item_c in self.items:
                if item_c.production == item.production and item_c.index == item.index + 1:
                    node.add_transition(
                        item.production.body[item.index], self.item_to_node[item_c.ind])

    def build_table(self, name: str) -> bool:
        node_actions = []
        self.grammar.calculate_follow()
        result = True

        for node in self.nodes:
            node_action = NodeAction(node.ind)

            for t, i in node.transitions.items():
                if t.is_terminal:
                    result = result and node_action.add_terminal_action(
                        t, Action.SHIFT, i)
                else:
                    result = result and node_action.add_no_terminal_action(
                        t, i)

            for item in node.items:
                if item.index == len(item.production.body):
                    if item.production.head == self.grammar.main:
                        result = result and node_action.add_terminal_action(
                            EOF(), Action.ACCEPT, -1)
                    else:
                        for t in self.grammar.follows[item.production.head]:
                            result = result and node_action.add_terminal_action(
                                t, Action.REDUCE, item.production.ind)

            node_actions.append(node_action)

        if result:
            TableLR.build(name, node_actions)

        return result
