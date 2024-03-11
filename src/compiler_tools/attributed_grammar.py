from typing import Generic, TypeVar, Dict, Callable, List, Tuple
from .grammar import GrammarToken, EOF
from .parser_out import DerivationTree

T1 = TypeVar('T1')
T2 = TypeVar('T2')


class AttributedRule(Generic[T1, T2]):
    def __init__(self, header_action: Callable[[List[T1], List[T1 | T2]], T1], actions: List[Tuple[int, Callable[[List[T1], List[T1 | GrammarToken]], T1]]] = []) -> None:
        self.actions: Dict[int, Callable[[List[T1 | T2], List[T1 | T2]], T1]] = {
            i: action for i, action in actions}
        self.header_action: Callable[[
            List[T1], List[T1 | T2]], T1] = header_action


class AttributedGrammar(Generic[T1, T2]):
    def __init__(self, rules: List[AttributedRule]) -> None:
        self.rules: List[AttributedRule] = rules
        self.terminals: List[GrammarToken] = []

    def evaluate(self, derivation_tree: DerivationTree, tokens: List[T2]) -> T1:
        self.terminals = tokens.copy()
        self.terminals.reverse()

        return self.__evaluate(derivation_tree)

    def __get_terminal(self) -> GrammarToken:
        t = self.terminals[-1]
        self.terminals.pop()

        return t

    def __evaluate(self, node: DerivationTree, inherit: T1 | None = None) -> T1:
        h: List[None | T1] = [inherit] + \
            [None for _ in range(len(node.children))]
        s: List[None | T1 | T2] = [None] + \
            [None for _ in range(len(node.children))]

        rule = self.rules[node.production_ind]

        for i, n in enumerate(node.children):
            if n.token == EOF():
                continue
            if n.token.is_terminal:
                s[i+1] = self.__get_terminal()
            else:
                if i in rule.actions:

                    h[i+1] = rule.actions[i](h, s)

                s[i+1] = self.__evaluate(n, h[i+1])

        return rule.header_action(h, s)
