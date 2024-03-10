from abc import ABC, abstractproperty
from compiler_tools.automaton import Automaton, pattern_to_automaton


class MatchResult():
    def __init__(self, value: str | None = None, error: str = '') -> None:
        self.value: str | None = value
        self.ok = value is not None
        self.error: str = error


class RegexAst(ABC):
    @abstractproperty
    def automaton(self) -> Automaton:
        pass


class RegexOr(RegexAst):
    def __init__(self, left: RegexAst, right: RegexAst) -> None:
        super().__init__()
        self.left: RegexAst = left
        self.right: RegexAst = right

    @property
    def automaton(self) -> Automaton:
        return self.left.automaton.join(self.right.automaton)


class RegexConcat(RegexAst):
    def __init__(self, left: RegexAst, right: RegexAst) -> None:
        super().__init__()
        self.left: RegexAst = left
        self.right: RegexAst = right

    @property
    def automaton(self) -> Automaton:
        return self.left.automaton.concat(self.right.automaton)


class RegexQuestion(RegexAst):
    def __init__(self, body: RegexAst) -> None:
        super().__init__()

        self.body: RegexAst = body

    @property
    def automaton(self) -> Automaton:
        return pattern_to_automaton('').join(self.body.automaton)


class RegexMany(RegexAst):
    def __init__(self, body: RegexAst) -> None:
        super().__init__()

        self.body: RegexAst = body

    @property
    def automaton(self) -> Automaton:
        return self.body.automaton.many()


class RegexOneAndMany(RegexAst):
    def __init__(self, body: RegexAst) -> None:
        super().__init__()

        self.body: RegexAst = body

    @property
    def automaton(self) -> Automaton:
        return self.body.automaton.concat(self.body.automaton.many())


class RegexChar(RegexAst):
    def __init__(self, char: str) -> None:
        super().__init__()

        self.char: str = char

    @property
    def automaton(self) -> Automaton:
        return pattern_to_automaton(self.char)


class RegexAnyChar(RegexAst):
    @property
    def automaton(self):
        a = Automaton()
        new_state = a.get_new_state()
        a.add_complement(a.initial_state, new_state)
        a.add_final_state(new_state)

        return a


class RegexRank(RegexAst):
    def __init__(self, left: str, right: str) -> None:
        super().__init__()

        self.left: str = left
        self.right: str = right

    @property
    def automaton(self):
        ind = ord(self.left)

        r = Automaton()

        while ind <= ord(self.right):
            r.join(pattern_to_automaton(chr(ind)))
            ind += 1

        return r

    # def match(self, text: str, index: int = 0) -> MatchResult:
    #     if index < len(text) and ord(self.left) <= ord(text[index]) and ord(text[index]) <= ord(self.right):
    #         return MatchResult(text[index])

    #     return MatchResult(error='Invalid character')


class RegexNot(RegexAst):
    def __init__(self, body: RegexAst) -> None:
        super().__init__()

        self.body: RegexAst = body

    @property
    def automaton(self):
        dfa = self.body.automaton.to_dfa()
        new_state = dfa.get_new_state()
        dfa.add_final_state(new_state)
        dfa.add_complement(dfa.initial_state, new_state)

        for s in dfa.states:
            if s == new_state:
                continue

            if s.is_final:
                s.is_final = False

        return dfa
