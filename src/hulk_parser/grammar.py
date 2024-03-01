from typing import List, Dict, Set


class GrammarToken:
    def __init__(self, value: str, is_terminal: bool = False, is_main: bool = False) -> None:
        self.value: str = value
        self.is_terminal: str = is_terminal and not is_main
        self.is_main: str = is_main

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return self.value


class EOF(GrammarToken):
    def __init__(self) -> None:
        super().__init__("EOF", True)


class GrammarProduction:
    def __init__(self, ind: int, head: GrammarToken, body: List[GrammarToken]) -> None:
        self.head: GrammarToken = head
        self.body: List[GrammarToken] = body
        self.ind = ind


class Grammar:
    def __init__(self) -> None:
        self.productions: List[GrammarProduction] = []
        self.terminals: List[GrammarToken] = [EOF()]
        self.non_terminals: List[GrammarToken] = []
        self.firsts: Dict[GrammarToken, Set[GrammarToken]] = {}
        self.follows: Dict[GrammarToken, Set[GrammarToken]] = {}

    def get_production(self, ind: int) -> GrammarProduction:
        return self.productions[ind]

    def add_main(self, non_terminal: str) -> None:
        self.main = self.add_non_terminal(non_terminal)
        self.main.is_main = True

    def add_production(self, non_terminal: str, sentences: List[str]) -> None:
        head = self.add_non_terminal(non_terminal)

        for sentence in sentences:
            tokens = sentence.split(" ")
            body = [EOF() if token == "" or token ==
                    "EOF" else self.add_terminal(token) for token in tokens]

            self.productions.append(GrammarProduction(
                len(self.productions), head, body))

    def add_non_terminal(self, value: str) -> GrammarToken:
        token = GrammarToken(value, False)

        if token not in self.non_terminals:
            self.non_terminals.append(token)

        if token in self.terminals:
            self.terminals.remove(token)

        return token

    def add_terminal(self, value: str) -> GrammarToken:
        token = GrammarToken(value, True)

        if token in self.non_terminals:
            token.is_terminal = False
            return token

        if token not in self.terminals:
            self.terminals.append(token)

        return token

    def calculate_first(self) -> List[GrammarToken]:
        for terminal in self.terminals:
            self.firsts[terminal] = {terminal}

        for non_terminal in self.non_terminals:
            self.firsts[non_terminal] = set()

        changed = True

        while changed:
            changed = False

            for production in self.productions:
                head = production.head
                body = production.body

                all_epsilon = True
                for token in body:
                    for first in self.firsts[token]:
                        if first not in self.firsts[head]:
                            self.firsts[head].add(first)
                            changed = True

                    if EOF() not in self.firsts[token]:
                        all_epsilon = False
                        break

                if all_epsilon and EOF() not in self.firsts[head]:
                    self.firsts[head].add(EOF())
                    changed = True

    def calculate_sentence_first(self, tokens: List[GrammarToken]) -> List[GrammarToken]:
        result = set()

        all_epsilon = True
        for token in tokens:
            for first in self.firsts[token]:
                result.add(first)

            if EOF() not in self.firsts[token]:
                all_epsilon = False
                break

        if all_epsilon and EOF() not in result:
            result.add(EOF())

        return result

    def calculate_follow(self) -> List[GrammarToken]:
        for non_terminal in self.non_terminals:
            self.follows[non_terminal] = set()

        self.follows[[token for token in self.non_terminals if token.is_main][0]].add(
            EOF())

        changed = True

        while changed:
            changed = False

            for production in self.productions:
                head = production.head
                body = production.body

                for i, token in enumerate(body):
                    if token.is_terminal:
                        continue

                    firsts = self.calculate_sentence_first(body[i+1:])
                    for first in firsts:
                        if first == EOF():
                            continue

                        if first not in self.follows[token]:
                            self.follows[token].add(first)
                            changed = True

                        if EOF() in firsts or i == len(body)-1:
                            for follow in self.follows[head]:
                                if follow not in self.follows[token]:
                                    self.follows[token].add(follow)
                                    changed = True
