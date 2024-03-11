from .grammar import GrammarProduction, GrammarToken, Grammar, EOF
from typing import List, Dict, Set, Tuple
from .tableLR import TableLR, NodeAction, Action
from typing import Generic, TypeVar
from abc import ABC, abstractmethod
from .itemLR import ItemLR
from queue import Queue

T = TypeVar('T', bound='ItemLR')


class Node(Generic[T]):
    def __init__(self, ind: int, items: Set[T]) -> None:
        self.ind: int = ind
        self.items: Set[int] = items
        self.transitions: Dict[GrammarToken, int] = {}

    def add_transition(self, token: GrammarToken, node: 'Node') -> None:
        self.transitions[token] = node.ind

    def __str__(self) -> str:
        s = ''

        for i in self.items:
            s += f'{str(i)}\n'

        return s


class AutomatonLR(ABC, Generic[T]):
    def __init__(self, name: str, grammar: Grammar):
        self.grammar: Grammar = grammar
        self.grammar.calculate_follow()

        self.items: List[T] = []
        self.nodes: List[Node] = []

        self._build_items()
        self._build_nodes()

        self.ok = self._build_table(name)

    def nodes_to_str(self):
        s = ''

        for n in self.nodes:
            s += f'{str(n)}\n'

        return s

    @abstractmethod
    def _get_item(self, production: GrammarProduction, index: int) -> T:
        pass

    @abstractmethod
    def _build_items(self):
        pass

    def _get_node(self, closure: Set[T]):
        node = Node(len(self.nodes), closure)
        self.nodes.append(node)

        return node

    @abstractmethod
    def _get_item_main(self) -> T:
        pass

    def _build_nodes(self):
        item_main = self._get_item_main()

        items_main = set([item_main])
        self._build_closure(items_main)
        node = self._get_node(items_main)

        q = Queue()
        q.put(node)

        while not q.empty():
            node = q.get()

            for t in self.grammar.get_tokens():
                if t == EOF():
                    continue

                goto = self._build_goto(node.items, t)

                if len(goto) == 0:
                    continue

                node_goto, to_add = self._get_goto_node(goto)
                node.add_transition(t, node_goto)

                if to_add:
                    q.put(node_goto)

    def _build_closure(self, items: Set[T]):
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

    def _build_goto(self, items: Set[T], token: GrammarToken) -> Set[T]:
        goto = set()

        for item in items:
            for item_g in item.get_transitions(token):
                item_g = self.items[item_g]
                goto.add(item_g)

        self._build_closure(goto)

        return goto

    def _get_goto_node(self, items: Set[T]) -> Tuple[Node, bool]:
        for node in self.nodes:
            if all(item in node.items for item in items) and len(node.items) == len(items):
                return node, False

        return self._get_node(items), True

    def _build_table(self, name: str) -> bool:
        node_actions = []
        result = True

        for node in self.nodes:
            node_action = NodeAction(node.ind)

            result = self._build_shift(node, node_action, result)
            result = self._build_reduce(node, node_action, result)

            node_actions.append(node_action)

        if result:
            TableLR.build(name, node_actions)

        return result

    def _build_shift(self, node: Node, node_action: NodeAction, result: bool):
        for t, i in node.transitions.items():
            if t.is_terminal:
                result = result and node_action.add_terminal_action(
                    t, Action.SHIFT, i)
            else:
                result = result and node_action.add_no_terminal_action(
                    t, i)

        return result

    @abstractmethod
    def _build_reduce(self, node: Node, node_action: NodeAction, result: bool) -> bool:
        pass
