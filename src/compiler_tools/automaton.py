from typing import Dict, Set, List, Tuple
from queue import Queue
import json


class State:
    def __init__(self, ind: int, is_final=False) -> None:
        self.ind = ind
        self.is_final: bool = is_final
        self.transitions: Dict[str, 'State'] = {}
        self.eof_transitions: Set['State'] = set()
        self.complement_state: State = None

    def add_transition(self, symbol: str, state: 'State') -> None:
        self.transitions[symbol] = state

    def add_eof_transition(self, state: 'State') -> None:
        self.eof_transitions.add(state)

    def goto(self, symbol: str) -> 'State | None':
        if symbol in self.transitions:
            return self.transitions[symbol]

        return self.complement_state

    def goto_eof(self) -> List['State']:
        return [s for s in self.eof_transitions]

    def __str__(self) -> str:
        return f'q{self.ind}'

    def __hash__(self) -> int:
        return self.ind

    def __eq__(self, o: object) -> bool:
        return self.ind == o.ind

    def to_json(self):
        result = {}

        for k, v in self.transitions.items():
            if not k in result:
                result[k] = []
            result[k].append(v.ind)

        result["eof"] = []

        for v in self.eof_transitions:
            result['eof'].append(v.ind)

        if self.complement_state is not None:
            result["default"] = self.complement_state.ind

        result["is_final"] = self.is_final

        return result


class Automaton:
    def __init__(self, copy=False) -> None:
        self.initial_state: State = None if copy else State(0)

        self.states: List[State] = []if copy else [self.initial_state]

    def add_transition(self, from_state: State, symbol: str, to_state: State) -> None:
        from_state.add_transition(symbol, to_state)

    def add_eof_transition(self, from_state: State, to_state: State) -> None:
        from_state.add_eof_transition(to_state)

    def add_final_state(self, state: State) -> None:
        state.is_final = True

    def add_complement(self, from_state: State, to_state: State) -> None:
        from_state.complement_state = to_state

    def get_new_state(self, state=None) -> State:
        new_state = state if state is not None else State(
            len(self.states))
        new_state.ind = len(self.states)

        self.states.append(new_state)
        return new_state

    @property
    def final_states(self) -> List[State]:
        return [state for state in self.states if state.is_final]

    def match(self, string: str) -> bool:
        visited = set([])
        return self.__match(self.initial_state, string, 0, visited)

    def __match(self, state: State, string: str, index, visited: Set[Tuple[int, int]]) -> bool:
        if (state.ind, index) in visited:
            return False

        visited.add((state.ind, index))

        if index == len(string):
            return state.is_final

        for eof_state in state.eof_transitions:
            if self.__match(eof_state, string, index, visited):
                return True

        goto = state.goto(string[index])

        if goto is not None:
            return self.__match(goto, string, index+1, visited)

        return False

    def join(self, automaton: 'Automaton') -> 'Automaton':
        automaton = automaton.copy()
        self.add_eof_transition(self.initial_state, automaton.initial_state)

        for state in automaton.states:
            self.get_new_state(state)

        return self

    def concat(self, automaton: 'Automaton') -> 'Automaton':
        automaton = automaton.copy()
        for state in self.final_states:
            self.add_eof_transition(state, automaton.initial_state)
            state.is_final = False

        for state in automaton.states:
            self.get_new_state(state)

        return self

    def many(self) -> 'Automaton':
        for state in self.final_states:
            self.add_eof_transition(state, self.initial_state)

        self.initial_state.is_final = True

        return self

    def copy(self) -> 'Automaton':
        new_automaton = Automaton(True)

        for _ in range(len(self.states)):
            new_automaton.get_new_state()

        new_automaton.initial_state = new_automaton.states[self.initial_state.ind]

        for state in self.states:
            for eof_state in state.eof_transitions:
                new_automaton.add_eof_transition(
                    new_automaton.states[state.ind], new_automaton.states[eof_state.ind])

            for symbol, symbol_state in state.transitions.items():
                new_automaton.add_transition(
                    new_automaton.states[state.ind], symbol, new_automaton.states[symbol_state.ind])

            new_automaton.states[state.ind].is_final = state.is_final
            new_automaton.states[state.ind].complement_state = None if state.complement_state is None else new_automaton.states[
                state.complement_state.ind]

        return new_automaton

    def to_dfa(self) -> 'Automaton':
        new_automaton = Automaton()
        new_nodes: List[Tuple[State, Set[State]]] = []

        initial = set([self.initial_state])
        self.__goto_eof(initial)
        new_nodes.append((new_automaton.initial_state, initial))

        new_automaton.initial_state.is_final = any(
            state for state in initial if state.is_final)

        q: Queue[Tuple[Automaton, Set[State]]] = Queue()
        q.put(new_nodes[0])

        while not q.empty():
            node, states = q.get()

            symbols = set([])
            for state in states:
                for s in state.transitions:
                    symbols.add(s)

            for symbol in symbols:
                goto = self.__goto_symbol(states, symbol)

                self.__next_goto(goto, new_automaton, node,
                                 new_nodes, q, symbol)

            goto = self.__goto_complement(states)
            self.__next_goto(goto, new_automaton, node, new_nodes, q)

        return new_automaton

    def __next_goto(self, goto: Set[State], new_automaton: 'Automaton', node: State, new_nodes: List[Tuple[State, Set[State]]], q: Queue, symbol: str | None = None):
        if len(goto) == 0:
            return

        new_node = self.__get_node(new_nodes, goto)

        if new_node is None:
            new_node = new_automaton.get_new_state()

            if any(state.is_final for state in goto):
                new_automaton.add_final_state(new_node)

            new_nodes.append((new_node, goto))
            q.put((new_node, goto))

        if symbol is not None:
            new_automaton.add_transition(node, symbol, new_node)
        else:
            new_automaton.add_complement(node, new_node)

    def __get_node(self, nodes: List[Tuple[State, Set[State]]], states: Set[State]) -> State | None:
        for node, node_states in nodes:
            if all(state in node_states for state in states) and len(node_states) == len(states):
                return node

        return None

    def __goto_complement(self, states: Set[State]) -> Set[State]:
        goto = set([])

        for state in states:
            if state.complement_state is None:
                continue

            goto.add(state.complement_state)

        self.__goto_eof(goto)

        return goto

    def __goto_eof(self, states: Set[State]):
        change = True

        while change:
            change = False
            aux = []

            for state in states:
                for eof_state in state.goto_eof():
                    if eof_state not in states:
                        aux.append(eof_state)

            for state in aux:
                change = True
                states.add(state)

    def __goto_symbol(self, states: Set[State], symbol: str) -> Set[State]:
        goto = set()

        for state in states:
            symbol_state = state.goto(symbol)
            if symbol_state is None:
                continue
            goto.add(symbol_state)

        self.__goto_eof(goto)

        return goto

    def load(self, name: str):
        cache = json.load(open(f"cache/{name}_automaton.json"))
        self.from_json(cache)

    def build(self, name: str):
        cache = self.to_json()
        json.dump(cache, open(f"cache/{name}_automaton.json", 'w'))

    def to_json(self):
        result = []

        for v in self.states:
            result.append(v.to_json())

        return result

    def from_json(self, json_dict):
        self.states.clear()

        for _ in range(len(json_dict)):
            self.get_new_state()

        for i, s in enumerate(json_dict):
            for k, v in s.items():
                if k == "eok":
                    for n in v:
                        self.states[i].add_eof_transition(self.states[n])
                    continue

                if k == "default":
                    self.states[i].complement_state = self.states[v]
                    continue

                if k == 'is_final':
                    self.states[i].is_final = v
                    continue

                for n in v:
                    self.states[i].add_transition(k, self.states[n])

        self.initial_state = self.states[0]


def pattern_to_automaton(pattern: str) -> Automaton:
    automaton = Automaton()

    state = automaton.initial_state

    for symbol in pattern:
        new_state = automaton.get_new_state()
        automaton.add_transition(state, symbol, new_state)
        state = new_state

    automaton.add_final_state(state)

    return automaton
