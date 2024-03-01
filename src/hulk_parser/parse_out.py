from .grammar import GrammarToken, Grammar, GrammarProduction
from typing import List


class DerivationTree:
    def __init__(self, token: GrammarToken, father: 'DerivationTree' | None = None) -> None:
        self.token: GrammarToken = token
        self.children: List[DerivationTree] = []
        self.father: DerivationTree | None = father

    def add_child(self, child: 'DerivationTree'):
        self.children.append(child)

    def set_father(self, father: 'DerivationTree'):
        self.father = father


class ParseResult:
    def __init__(self, derivations: List[GrammarProduction], error: int = -1) -> None:
        self.ok: bool = error != -1
        self.derivation_tree= ParseResult.__build_tree(derivations) if self.ok else None

    def __build_tree(derivations: List[GrammarProduction]) -> DerivationTree:
        root = DerivationTree(derivations[0].head)
        ParseResult.__build_tree_node(root, derivations, 0)

        return root

    def __build_tree_node(node: DerivationTree, derivations: List[GrammarProduction], index: int) -> int:
        tokens = derivations[index].body.copy()
        tokens.reverse()

        for token in tokens:
            if token.is_terminal:
                node.add_child(DerivationTree(token, node))
            else:
                child = DerivationTree(token, node)
                node.add_child(child)

                index = ParseResult.__build_tree_node(
                    child, derivations, index + 1)

        return index
