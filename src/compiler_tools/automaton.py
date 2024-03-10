from typing import Dict, Set, List, Tuple
from queue import Queue


class State:
    def __init__(self, ind: int, is_final=False) -> None:
        self.ind = ind
        self.is_final: bool = is_final
        self.transitions: Dict[str, 'State'] = {}
        self.eof_transitions: Set['State'] = {}

    def add_transition(self, symbol: str, state: 'State') -> None:
        self.transitions[symbol] = state

    def add_eof_transition(self, state: 'State') -> None:
        self.eof_transitions.add(state)

    def goto(self, symbol: str) -> 'State' | None:
        if symbol in self.transitions:
            return self.transitions[symbol]

        return None

    def __str__(self) -> str:
        return f'q{self.ind}'

    def __hash__(self) -> int:
        return self.ind

    def __eq__(self, o: object) -> bool:
        return self.ind == o.ind


class Automaton:
    def __init__(self, initial_state=None) -> None:
        self.initial_state: State = initial_state if initial_state is not None else State(
            0)
        self.initial_state.ind = 0

        self.states: List[State] = [self.initial_state]
        self.symbols: Set[str] = set()

    def add_transition(self, from_state: State, symbol: str, to_state: State) -> None:
        from_state.add_transition(symbol, to_state)
        self.symbols.add(symbol)

    def add_eof_transition(self, from_state: State, to_state: State) -> None:
        from_state.add_eof_transition(to_state)

    def add_final_state(self, state: State) -> None:
        state.is_final = True

    def get_new_state(self, state=None) -> State:
        new_state = state if state is not None else State(len(self.states))
        new_state.ind = len(self.states)

        self.states.append(new_state)
        return new_state

    @property
    def final_states(self) -> List[State]:
        return [state for state in self.states if state.is_final]

    def match(self, string: str) -> bool:
        return self.__match(self.initial_state, string, 0)

    def __match(self, state: State, string: str, index) -> bool:
        if index == len(string):
            return state.is_final

        for eof_state in state.eof_transitions:
            if self.__match(eof_state, string, index):
                return True

        for symbol in state.transitions:
            if self.__match(state.transitions[symbol], string, index+1):
                return True

        return False

    def join(self, automaton: 'Automaton'):
        self.add_eof_transition(self.initial_state, automaton.initial_state)

        for state in automaton.states:
            self.get_new_state(state)

    def concat(self, automaton: 'Automaton'):
        for state in self.final_states:
            self.add_eof_transition(state, automaton.initial_state)
            state.is_final = False

        for state in automaton.states:
            self.get_new_state(state)

    def complement(self):
        for state in self.states:
            state.is_final = not state.is_final

    def to_dfa(self) -> 'Automaton':
        new_automaton = Automaton()
        new_nodes: List[Tuple[State, Set[State]]] = []

        new_nodes.append((new_automaton.initial_state,
                         self.__goto_eof({self.initial_state})))

        q = Queue()
        q.put(new_nodes[0])

        while not q.empty():
            node, states = q.get()

            for symbol in self.symbols:
                goto = self.__goto_symbol(states, symbol)

                if len(goto) == 0:
                    continue

                new_node = self.__get_node(new_nodes, goto)

                if new_node is None:
                    new_node = (new_automaton.get_new_state(), goto)

                    if any(state.is_final for state in goto):
                        new_automaton.add_final_state(new_node[0])

                    new_nodes.append(new_node)
                    q.put(new_node)

                self.add_transition(node, symbol, new_node[0])

        return new_automaton

    def __get_node(self, nodes: List[Tuple[State, Set[State]]], states: Set[State]) -> State | None:
        for node, node_states in nodes:
            if all(state in node_states for state in states):
                return node

        return None

    def __goto_eof(self, states: Set[State]):
        change = True

        while change:
            change = False
            aux = []

            for state in states:
                for eof_state in state.eof_transitions:
                    if eof_state not in states:
                        aux.append(eof_state)

            for state in aux:
                change = True
                states.add(state)

    def __goto_symbol(self, states: Set[State], symbol: str) -> Set[State]:
        goto = set()

        for state in states:
            if symbol in state.transitions:
                goto.add(state.transitions[symbol])

        self.__goto_eof(goto)

        return goto


def pattern_to_automaton(pattern: str) -> Automaton:
    automaton = Automaton()

    state = automaton.initial_state

    for symbol in pattern:
        new_state = automaton.get_new_state()
        automaton.add_transition(state, symbol, new_state)
        state = new_state

    automaton.add_final_state(state)

    return automaton
