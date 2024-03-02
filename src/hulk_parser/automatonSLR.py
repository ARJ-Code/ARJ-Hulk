from .grammar import GrammarProduction, GrammarToken, Grammar, EOF
from typing import List, Dict, Set
from .tableLR import TableLR, NodeAction, Action
from .automaton import AutomatonNFA


class ItemLR:
    def __init__(self, ind: int, production: GrammarProduction, index: int) -> None:
        self.production: GrammarProduction = production
        self.index: int = index
        self.ind = ind

    def __eq__(self, other) -> bool:
        self.ind == other.ind

    def __hash__(self) -> int:
        return self.ind

    def __str__(self) -> str:
        return str(self.production)+' '+str(self.index)


class NodeLR:
    def __init__(self, ind: int, items: List[ItemLR]) -> None:
        self.ind: int = ind
        self.items: List[ItemLR] = items
        self.transitions: Dict[GrammarToken, int] = {}

    def add_transition(self, token: GrammarToken, node: 'NodeLR') -> None:
        self.transitions[token] = node.ind

    def __str__(self) -> str:
        s=''

        for i in self.items:
            s+=f'{str(i)}\n'

        return s

class AutomatonSLR:
    def __init__(self, name: str, grammar: Grammar):
        self.grammar: Grammar = grammar
        self.items: List[ItemLR] = []
        self.nodes: List[NodeLR] = []

        nfa = self.build_items()
        self.build_nodes(nfa)

        self.build_table(name)

    def nodes_to_str(self):
        s = ''

        for n in self.nodes:
            s+=f'{str(n)}\n'

        return s

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
                    nfa.add_transition(
                        x.ind, y.ind, x.production.body[x.index])

        return nfa

    def build_nodes(self, nfa: AutomatonNFA):
        dfa = nfa.compute_dfa()

        for l in dfa.sets:
            items = [self.items[i] for i in l]
            self.get_node(set(items))

        for i in range(len(self.nodes)):
            for k, v in dfa.transitions[i].items():
                self.nodes[i].add_transition(
                    k, self.nodes[v])

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
