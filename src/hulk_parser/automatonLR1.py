from .grammar import GrammarProduction, GrammarToken, Grammar, EOF
from typing import List, Dict, Set
from .tableLR import TableLR, NodeAction, Action
from .automaton import AutomatonNFA


class ItemLR1:
    def __init__(self, ind: int, production: GrammarProduction, index: int, teal: GrammarToken) -> None:
        self.production: GrammarProduction = production
        self.index: int = index
        self.ind = ind
        self.teal = teal

    def __eq__(self, other) -> bool:
        self.ind == other.ind

    def __hash__(self) -> int:
        return self.ind

    def __str__(self) -> str:
        return str(self.production)+' '+str(self.index)+' '+str(self.teal)


class NodeLR1:
    def __init__(self, ind: int, items: List[ItemLR1]) -> None:
        self.ind: int = ind
        self.items: List[ItemLR1] = items
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

        nfa = self.build_items()
        self.build_nodes(nfa)

        self.build_table(name)

    def nodes_to_str(self):
        s = ''

        for n in self.nodes:
            s += f'{str(n)}\n'

        return s

    def get_item(self, production: GrammarProduction, index: int, teal: GrammarToken) -> ItemLR1:
        item = ItemLR1(len(self.items), production, index, teal)
        self.items.append(item)

        return item

    def get_node(self, closure: Set[ItemLR1]):
        node = NodeLR1(len(self.nodes), closure)
        self.nodes.append(node)

        return node

    def build_items(self) -> AutomatonNFA:
        for production in self.grammar.productions:
            for i in range(len(production.body) + 1):
                for t in self.grammar.terminals:
                    self.get_item(production, i, t)

        nfa = AutomatonNFA(len(self.items))

        for x in self.items:
            for y in self.items:
                if x.index == len(x.production.body):
                    continue

                if y.production.head == x.production.body[x.index] and y.index == 0:
                    w = self.grammar.calculate_sentence_first(
                        x.production.body[x.index+1:])
                    if x.teal in w:
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
        
        print(len(self.nodes))

        for i in range(len(self.nodes)):
            for k, v in dfa.transitions[i].items():
                self.nodes[i].add_transition(
                    k, self.nodes[v])

    def build_table(self, name: str) -> bool:
        node_actions = []
        result = True

        for node in self.nodes:
            node_action = NodeAction(node.ind)

            for t, i in node.transitions.items():
                if t.is_terminal:
                    result = result and node_action.add_terminal_action(
                        t, Action.SHIFT, i)
                    if not result:
                        print('1')
                else:
                    result = result and node_action.add_no_terminal_action(
                        t, i)
                    if not result:
                        print('2')
               

            for item in node.items:
                if item.index == len(item.production.body):
                    if item.production.head == self.grammar.main:
                        result = result and node_action.add_terminal_action(
                            EOF(), Action.ACCEPT, -1)
                        if not result:
                            print('3')
               
                    else:
                        result = result and node_action.add_terminal_action(
                            item.teal, Action.REDUCE, item.production.ind)
                        if not result:
                            print('4')

            node_actions.append(node_action)

        if result:
            TableLR.build(name, node_actions)

        return result
