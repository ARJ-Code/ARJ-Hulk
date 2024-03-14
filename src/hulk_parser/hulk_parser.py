from compiler_tools.automatonLR1 import AutomatonLR1
from .hulk_grammar import hulk_grammar


def hulk_build():
    a = AutomatonLR1('hulk', hulk_grammar)
    return a.ok
