from .grammar import GrammarProduction, GrammarToken, Grammar, EOF
from typing import List, Dict, Set
from .tableLR import TableLR, NodeAction, Action


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
        return str(self.production)+' '+str(self.index)

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


class NodeLR:
    def __init__(self, ind: int, items: Set[ItemLR]) -> None:
        self.ind: int = ind
        self.items: Set[ItemLR] = items
        self.transitions: Dict[GrammarToken, int] = {}

    def add_transition(self, token: GrammarToken, node: 'NodeLR') -> None:
        self.transitions[token] = node.ind

    def __str__(self) -> str:
        s = ''

        for i in self.items:
            s += f'{str(i)}\n'

        return s


class AutomatonSLR:
    def __init__(self, name: str, grammar: Grammar):
        self.grammar: Grammar = grammar
        self.grammar.calculate_follow()

        self.items: List[ItemLR] = []
        self.nodes: List[NodeLR] = []

        self.build_items()
        self.build_nodes()

        self.build_table(name)

    def nodes_to_str(self):
        s = ''

        for n in self.nodes:
            s += f'{str(n)}\n'

        return s

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
        item_main = [
            item for item in self.items if item.production.head == self.grammar.main and item.index == 0]

        items_main = set(item_main)
        self.build_closure(items_main)
        node = self.get_node(items_main)

        change = True

        while change:
            change = False
            for node in self.nodes:
                for t in self.grammar.get_tokens():
                    if t == EOF():
                        continue

                    if t in node.transitions:
                        continue

                    goto = self.build_goto(node.items, t)

                    if len(goto) == 0:
                        continue

                    node_goto = self.get_goto_node(goto)
                    node.add_transition(t, node_goto)

                    change = True

    def build_closure(self, items: Set[ItemLR]):
        change = True

        while change:
            aux = []

            for item in items:
                for item_c in item.get_eof_transitions():
                    item_c = self.items[item_c]

                    if item_c in items:
                        continue

                    aux.append(item_c)

            for item in aux:
                items.add(item)

            change = len(aux) != 0

    def build_goto(self, items: Set[ItemLR], token: GrammarToken) -> Set[ItemLR]:
        goto = set()

        for item in items:
            for item_g in item.get_transitions(token):
                item_g = self.items[item_g]
                goto.add(item_g)

        self.build_closure(goto)

        return goto

    def get_goto_node(self, items: Set[ItemLR]) -> NodeLR:
        for node in self.nodes:
            if all(item in node.items for item in items):
                return node

        return self.get_node(items)

    def build_table(self, name: str) -> bool:
        node_actions = []
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
