from compiler_tools.automatonLR1 import AutomatonLR1
from .hulk_grammar import hulk_grammar
from compiler_tools.grammar import GrammarToken
from compiler_tools.parser import Parser
from compiler_tools.tableLR import TableLR


def hulk_build():
    a = AutomatonLR1('hulk', hulk_grammar)
    return a.ok


def hulk_parse():
    t = TableLR(hulk_grammar)
    t.load('hulk')

    p = Parser(hulk_grammar, t)

    r = p.parse([GrammarToken('num', True), GrammarToken('*', True), GrammarToken('num', True),
                GrammarToken('+', True), GrammarToken('num', True), GrammarToken('*', True), GrammarToken('num', True), GrammarToken(';', True)])
    print(r.ok)
