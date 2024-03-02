from .grammar import GrammarProduction, GrammarToken, Grammar, EOF
from typing import List, Dict, Set
from .tableLR import TableLR, NodeAction, Action


class ItemLR1:
    def __init__(self, ind: int, production: GrammarProduction, index: int, teal: GrammarToken) -> None:
        self.production: GrammarProduction = production
        self.index: int = index
        self.ind = ind
        self.teal = teal
        self.transitions: Dict[GrammarToken, Set[int]] = {}

    def __eq__(self, other) -> bool:
        self.ind == other.ind

    def __hash__(self) -> int:
        return self.ind

    def __str__(self) -> str:
        return f"{self.production} {self.index} {self.teal}"

    def add_transition(self, token: GrammarToken, item: 'ItemLR1'):
        if token not in self.transitions:
            self.transitions[token] = set()

        self.transitions[token].add(item.ind)

    def add_eof_transition(self, item: 'ItemLR1'):
        self.add_transition(EOF(), item)

    def get_transitions(self, token: GrammarToken) -> List[int]:
        if token not in self.transitions:
            return []

        return list(self.transitions[token])

    def get_eof_transitions(self) -> List[int]:
        return self.get_transitions(EOF())


class NodeLR1:
    def __init__(self, ind: int, items: Set[ItemLR1]) -> None:
        self.ind: int = ind
        self.items: Set[ItemLR1] = items
        self.transitions: Dict[GrammarToken, int] = {}

    def add_transition(self, token: GrammarToken, node: 'NodeLR1') -> None:
        self.transitions[token] = node.ind

    def __str__(self) -> str:
        s = ''

        for i in self.items:
            s += f'{str(i)}\n'

        return s


class AutomatonLR1:
    def __init__(self, name: str, grammar: Grammar):
        self.grammar: Grammar = grammar
        self.grammar.calculate_first()

        self.items: List[ItemLR1] = []
        self.nodes: List[NodeLR1] = []

        self.__build_items()
        self.__build_nodes()

        self.ok = self.__build_table(name)

    def nodes_to_str(self):
        s = ''

        for n in self.nodes:
            s += f'{str(n)}\n'

        return s

    def __get_item(self, production: GrammarProduction, index: int, teal: GrammarToken) -> ItemLR1:
        item = ItemLR1(len(self.items), production, index, teal)
        self.items.append(item)

        return item

    def __get_node(self, closure: Set[ItemLR1]):
        node = NodeLR1(len(self.nodes), closure)
        self.nodes.append(node)

        return node

    def __build_items(self):
        for production in self.grammar.productions:
            for i in range(len(production.body) + 1):
                for t in self.grammar.terminals:
                    self.__get_item(production, i, t)

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

    def __build_nodes(self):
        item_main = [
            item for item in self.items if item.production.head == self.grammar.main and item.index == 0 and item.teal == EOF()]

        items_main = set(item_main)
        self.__build_closure(items_main)
        node = self.__get_node(items_main)

        change = True

        while change:
            change = False
            for node in self.nodes:
                for t in self.grammar.get_tokens():
                    if t == EOF():
                        continue

                    if t in node.transitions:
                        continue

                    goto = self.__build_goto(node.items, t)

                    if len(goto) == 0:
                        continue

                    node_goto = self.__get_goto_node(goto)
                    node.add_transition(t, node_goto)

                    change = True

    def __build_closure(self, items: Set[ItemLR1]):
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

    def __build_goto(self, items: Set[ItemLR1], token: GrammarToken) -> Set[ItemLR1]:
        goto = set()

        for item in items:
            for item_g in item.get_transitions(token):
                item_g = self.items[item_g]
                goto.add(item_g)

        self.__build_closure(goto)

        return goto

    def __get_goto_node(self, items: Set[ItemLR1]) -> NodeLR1:
        for node in self.nodes:
            if all(item in node.items for item in items):
                return node

        return self.__get_node(items)

    def __build_table(self, name: str) -> bool:
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
                        result = result and node_action.add_terminal_action(
                            item.teal, Action.REDUCE, item.production.ind)

            node_actions.append(node_action)

        if result:
            TableLR.build(name, node_actions)

        return result
