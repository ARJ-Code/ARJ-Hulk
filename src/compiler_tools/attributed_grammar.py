from typing import Generic, TypeVar, Dict, Callable, List, Tuple
from .grammar import GrammarToken, EOF, Grammar
from .parser_out import DerivationTree

T1 = TypeVar('T1')
T2 = TypeVar('T2')


class AttributedRule(Generic[T1, T2]):
    def __init__(self, header_action: Callable[[List[T1], List[T1 | T2]], T1], actions: List[Tuple[int, Callable[[List[T1], List[T1 | GrammarToken]], T1]]] = []) -> None:
        self.actions: Dict[int, Callable[[List[T1 | T2], List[T1 | T2]], T1]] = {
            i: action for i, action in actions}
        self.header_action: Callable[[
            List[T1], List[T1 | T2]], T1] = header_action


class AttributedGrammar(Generic[T1, T2], Grammar):
    def __init__(self) -> None:
        super().__init__()
        self.rules: List[AttributedRule] = []

    def add_attributed_production(self, non_terminal: str, sentences: List[str], rules: List[AttributedRule]) -> None:
        super().add_production(non_terminal, sentences)
        self.rules += rules

    def evaluate(self, derivation_tree: DerivationTree, tokens: List[T2]) -> T1:
        tokens = tokens.copy()
        tokens.reverse()

        return self.__evaluate(derivation_tree, tokens)

    def __evaluate(self, node: DerivationTree, tokens: List[T2], inherit: T1 | None = None) -> T1:
        def get_terminal() -> GrammarToken:
            t = tokens[-1]
            tokens.pop()

            return t

        h: List[None | T1] = [inherit] + \
            [None for _ in range(len(node.children))]
        s: List[None | T1 | T2] = [None] + \
            [None for _ in range(len(node.children))]

        rule = self.rules[node.production_ind]

        for i, n in enumerate(node.children):
            if n.token.is_terminal:
                s[i+1] = get_terminal()
            else:
                if i in rule.actions:

                    h[i+1] = rule.actions[i](h, s)

                s[i+1] = self.__evaluate(n, tokens, h[i+1])

        return rule.header_action(h, s)
