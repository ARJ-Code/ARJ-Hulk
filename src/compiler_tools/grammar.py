from typing import List, Dict, Set, Generic, TypeVar

T = TypeVar('T')


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

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __str__(self) -> str:
        value = str(self.head)+" -> "

        for v in self.body:
            value += str(v)+" "

        return value

    def __hash__(self) -> int:
        return hash(str(self.ind))


class Grammar:
    def __init__(self) -> None:
        self.productions: List[GrammarProduction] = []
        self.terminals: Set[GrammarToken] = set([EOF()])
        self.non_terminals: Set[GrammarToken] = set()
        self.firsts: Dict[GrammarToken, Set[GrammarToken]] = {}
        self.follows: Dict[GrammarToken, Set[GrammarToken]] = {}

    def get_production(self, ind: int) -> GrammarProduction:
        return self.productions[ind]

    def get_tokens(self):
        for t in self.non_terminals:
            yield t

        for t in self.terminals:
            yield t

    def get_token(self, value: str) -> GrammarToken:
        for t in self.non_terminals:
            if t.value == value:
                return t

        for t in self.terminals:
            if t.value == value:
                return t

    def add_main(self, non_terminal: str) -> None:
        self.main = GrammarToken(non_terminal)
        self.main.is_main = True

        self.non_terminals.add(self.main)

    def add_production(self, non_terminal: str, sentences: List[str]) -> None:
        def get(t: str):
            if t == "" or t == "EOF":
                return EOF()

            t = GrammarToken(t, t[0].lower() == t[0])

            if t.is_terminal:
                self.terminals.add(t)
            else:
                self.non_terminals.add(t)

            if t == self.main:

                t = self.main

            return t

        if non_terminal[0] != non_terminal[0].upper():
            raise ValueError("Non terminal must be in upper case")

        head = get(non_terminal)

        for sentence in sentences:
            tokens = sentence.split(" ")
            body = [get(token)
                    for token in tokens if token != 'EOF' and token != '']

            self.productions.append(GrammarProduction(
                len(self.productions), head, body))

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
        self.calculate_first()

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


class AttributedGrammar(Grammar, Generic[T]):
    def __init__(self) -> None:
        super().__init__()
