from typing import Generic, TypeVar, Dict, Callable, List, Tuple
from .grammar import Grammar, GrammarToken
from .parser_out import DerivationTree

T = TypeVar('T')


class AttributedRule(Generic[T]):
    def __init__(self, header_action: Callable[[List[T], List[T | GrammarToken]], T], actions: List[Tuple[int, Callable[[List[T], List[T | GrammarToken]], T]]]) -> None:
        self.actions: Dict[int, Callable[[List[T | GrammarToken], List[T | GrammarToken]], T]] = {
            i: action for i, action in actions}
        self.header_action: Callable[[
            List[T], List[T | GrammarToken]], T] = header_action

    def __call__(self, stack: List[T], symbols: List[T]) -> T:
        return self.action(stack, symbols)


class AttributedGrammar(Generic[T]):
    def __init__(self, rules: List[AttributedRule]) -> None:
        self.rules: Dict[int, AttributedRule] = {i: rule for i, rule in rules}
        self.terminals: List[GrammarToken] = []

    def evaluate(self, derivation_tree: DerivationTree, tokens: List[GrammarToken]) -> T:
        self.terminals = tokens.copy()
        self.terminals.reverse()

        return self.evaluate(derivation_tree)

    def __get_terminal(self) -> GrammarToken:
        t = self.terminals[-1]
        self.terminals.pop()

        return t

    def __evaluate(self, node: DerivationTree, inherit: T | None = None) -> T:
        h: List[None | T] = [inherit] + \
            [None for _ in range(len(node.children))]
        s: List[None | T | GrammarToken] = [None] + \
            [None for _ in range(len(node.children))]

        rule = self.rules[node.production_ind]

        for i, n in enumerate(node.children):
            if n.token.is_terminal:
                s[i+1] = self.__get_terminal()
            else:
                if i in rule.actions:
                    h[i+1] = rule.actions[i](h, s)

                s[i+1] = self.__evaluate(n, h[i+1])

        return rule.header_action(h, s)
