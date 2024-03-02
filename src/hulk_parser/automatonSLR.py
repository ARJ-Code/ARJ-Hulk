from .grammar import GrammarProduction, GrammarToken, Grammar, EOF
from typing import List, Dict, Set, Tuple
from .tableLR import TableLR, NodeAction, Action
from queue import Queue
from .automaton import AutomatonNFA, AutomatonDFA


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

        nfa = self.build_items()
        self.build_nodes(nfa)

        self.build_table(name)

    def get_item(self, production: GrammarProduction, index: int) -> ItemLR:
        item = ItemLR(len(self.items), production, index)
        self.items.append(item)

        return item

    def get_node(self, closure: Set[ItemLR]):
        node = NodeLR(len(self.nodes), closure)
        self.nodes.append(node)

        return node

    def build_items(self) -> AutomatonNFA:
        for production in self.grammar .productions:
            for i in range(len(production.body) + 1):
                self.get_item(production, i)

        nfa = AutomatonNFA(len(self.items))

        for x in self.items:
            for y in self.items:
                if x.index == len(x.production.body):
                    continue

                if y.production.head == x.production.body[x.index] and y.index == 0:
                    nfa.add_epsilon_transition(x.ind, y.ind)

                if y.production == x.production and y.index == x.index + 1:
                    x.add_transition(x.production.body[x.index], y)
                    nfa.add_transition(
                        x.ind, y.ind, x.production.body[x.index].value)

        return nfa

    def build_nodes(self, nfa: AutomatonNFA):
        dfa = nfa.compute_dfa()

        for l in dfa.sets:
            items = [self.items[i] for i in l]
            self.get_node(set(items))

        for i in range(len(self.nodes)):
            for k, v in dfa.transitions[i].items():
                self.nodes[i].add_transition(
                    self.grammar.get_token(k), self.nodes[v])

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
