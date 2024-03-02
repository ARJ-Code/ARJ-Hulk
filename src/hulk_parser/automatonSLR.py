from .grammar import GrammarProduction, GrammarToken, Grammar, EOF
from typing import List, Dict, Set, Tuple
from .tableLR import TableLR, NodeAction, Action
from queue import Queue


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

    def add_transition(self, token: GrammarToken, item: 'ItemLR'):
        if token not in self.transitions:
            self.transitions[token] = set()

        self.transitions[token].add(item.ind)

    def add_eof_transition(self, item: 'ItemLR'):
        self.add_transition(EOF(), item)

    def get_transitions(self, token: GrammarToken) -> Set[int]:
        if token not in self.transitions:
            return set([])

        return self.transitions[token]

    def get_eof_transitions(self):
        return self.get_transitions(EOF())


class NodeLR:
    def __init__(self, ind: int, items: Set[ItemLR]) -> None:
        self.ind: int = ind
        self.items: Set[ItemLR] = items
        self.transitions: Dict[GrammarToken, int] = {}

    def contains(self, item: ItemLR) -> bool:
        return item in self.items

    # def add_item(self, item: ItemLR) -> None:
    #     self.items.add(item)

    def add_transition(self, token: GrammarToken, node: 'NodeLR') -> None:
        self.transitions[token] = node.ind


class AutomatonSLR:
    def __init__(self, name: str, grammar: Grammar):
        self.grammar: Grammar = grammar
        self.items: List[ItemLR] = []
        self.nodes: List[NodeLR] = []
        # self.item_to_node: List[NodeLR | None] = []

        self.build_items()
        self.build_nodes()

        self.build_table(name)

    def get_item(self, production: GrammarProduction, index: int) -> ItemLR:
        item = ItemLR(len(self.items), production, index)
        self.items.append(item)

        return item

    def get_node(self, closure: Set[ItemLR]):
        node = NodeLR(len(self.nodes), closure)
        self.nodes.append(node)

        return node

    def build_items(self):
        for production in self.grammar .productions:
            for i in range(len(production.body) + 1):
                self.get_item(production, i)

        for x in self.items:
            for y in self.items:
                if x.index == len(x.production.body):
                    continue

                if y.production.head == x.production.body[x.index] and y.index == 0:
                    x.add_eof_transition(y)

                if y.production == x.production and y.index == x.index + 1:
                    x.add_transition(x.production.body[x.index], y)

    def build_nodes(self):
        main_item = [item for item in self.items if item.production.head ==
                     self.grammar.main and item.index == 0][0]

        main_closure = set([main_item])
        self.build_closure(main_closure)

        self.get_node(main_closure)

        change = True

        while change:
            change = False

            for node in self.nodes:
                for token in self.grammar.get_tokens():
                    if token in node.transitions:
                        continue

                    goto_closure = self.build_goto(node.items, token)

                    if len(goto_closure) == 0:
                        continue

                    node_goto = self.closure_to_node(goto_closure)

                    node.add_transition(token, node_goto)
                    change = True

    def closure_to_node(self, closure: Set[ItemLR]):
        for node in self.nodes:
            if any([x for x in node.items if x in closure]):
                return node

        return self.get_node(closure)

    def build_closure(self, closure: Set[ItemLR]):
        change = True

        while change:
            aux = []

            for item in closure:
                for ind_c in item.get_eof_transitions():
                    item_c = self.items[ind_c]

                    if item_c in closure:
                        continue

                    aux.append(item_c)

            for item in aux:
                closure.add(item)

            change = len(aux) != 0

    def build_goto(self, closure: Set[ItemLR], token: GrammarToken) -> Set[NodeLR]:
        goto_closure = set()

        for item in closure:
            for ind_g in item.get_transitions(token):
                item_g = self.items[ind_g]

                goto_closure.add(item_g)

        self.build_closure(goto_closure)

        return goto_closure

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
