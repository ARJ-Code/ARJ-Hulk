from typing import List, Dict, Set, Tuple
from .grammar import GrammarToken, EOF


class DisjointSet:
    def __init__(self, n: int) -> None:
        self.parent = [i for i in range(n)]
        self.rank = [0 for _ in range(n)]

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        elif self.rank[x_root] > self.rank[y_root]:
            self.parent[y_root] = x_root
        else:
            self.parent[y_root] = x_root
            self.rank[x_root] += 1

    def is_same_set(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def get_set(self, x: int) -> List[int]:
        x_root = self.find(x)
        return [i for i in range(len(self.parent)) if self.find(i) == x_root]

    def cant_sets(self) -> int:
        return len([i for i in range(len(self.parent)) if self.find(i) == i])


class AutomatonDFA:
    def __init__(self, sets: List[List[int]]) -> None:
        self.sets: List[List[int]] = sets
        self.transitions: List[Dict[GrammarToken, int]] = [{} for _ in range(len(sets))]

    def add_transition(self, src: int, dest: int, token: GrammarToken) -> None:
        self.transitions[src][token] = dest


class AutomatonNFA:
    def __init__(self, n: int) -> None:
        self.n = n
        self.transitions: List[Dict[GrammarToken, List[int]]] = [{} for _ in range(n)]
        self.dsu = DisjointSet(n)
        self.tokens: Set[GrammarToken] = set()

    def add_transition(self, src: int, dest: int, token: GrammarToken) -> None:
        if token != EOF():
            self.tokens.add(token)

        if token not in self.transitions[src]:
            self.transitions[src][token] = []
        self.transitions[src][token].append(dest)

    def add_epsilon_transition(self, src: int, dest: int) -> None:
        self.add_transition(src, dest, EOF())

    def get_transitions(self, src, token: GrammarToken) -> List[int]:
        if token in self.transitions[src]:
            return self.transitions[src][token]
        return []

    def get_epsilon_transitions(self, src: int) -> List[int]:
        return self.get_transitions(src, EOF())

    def compute_dfa(self) -> AutomatonDFA:
        self.to_closure()
        self.to_goto()

        dfa, p = self.compute_sets()
        self.compute_transitions(dfa, p)

        return dfa

    def compute_sets(self) -> Tuple[AutomatonDFA, List[int]]:
        sets = []
        p = [0 for _ in range(self.n)]

        for i in range(self.n):
            if self.dsu.find(i) != i:
                continue

            for j in self.dsu.get_set(i):
                p[j] = len(sets)

            sets.append(self.dsu.get_set(i))

        return AutomatonDFA(sets), p

    def compute_transitions(self, dfa: AutomatonDFA, p: List[int]):
        for i in range(self.n):
            if self.dsu.find(i) != i:
                continue

            for s in self.dsu.get_set(i):
                for t in self.tokens:
                    for dest in self.get_transitions(s, t):
                        dfa.add_transition(p[i], p[dest], t)

    def to_closure(self):
        change = True

        while change:
            change = False
            mask_c = [False for _ in range(self.n)]

            for i in range(self.n):
                parent = self.dsu.find(i)

                if mask_c[parent]:
                    continue

                change = change or self.closure(parent)
                mask_c[parent] = True

    def to_goto(self):
        change = True

        while change:
            change = False
            mask_g = [False for _ in range(self.n)]

            for i in range(self.n):
                parent = self.dsu.find(i)

                if mask_g[parent]:
                    continue

                for t in self.tokens:
                    change = change or self.goto(parent, t)
                mask_g[parent] = True

    def closure(self, state: int) -> bool:
        l = self.dsu.get_set(state)
        change = False

        for s in l:
            for t in self.get_epsilon_transitions(s):
                if self.dsu.is_same_set(state, t):
                    continue

                self.dsu.union(state, t)
                change = True

        return change

    def goto(self, state: int, token: GrammarToken) -> bool:
        l = self.dsu.get_set(state)
        new_l = []
        change = False

        for s in l:
            for t in self.get_transitions(s, token):
                new_l.append(t)

        if len(new_l) == 0:
            return

        for i in new_l[1:]:
            if self.dsu.is_same_set(new_l[0], i):
                continue

            self.dsu.union(new_l[0], i)
            change = True

        return change
