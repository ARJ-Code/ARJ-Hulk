from hulk_parser.grammar import Grammar, GrammarToken
from hulk_parser.automatonSLR import AutomatonSLR
from hulk_parser.automatonLR1 import AutomatonLR1
from hulk_parser.tableLR import TableLR
from hulk_parser.parser import Parser

g = Grammar()

g.add_main("S")
g.add_production("S", ["E"])
g.add_production("E", ["T + E", "T"])
g.add_production("T", ["F * T","F"])
g.add_production("F",["n", "( E )"])
# g.add_production("F", ["( E )", "n"])
# g.add_production("E",["A = A","i"])
# g.add_production("A",["i + A","i"])

q = AutomatonSLR('test',g)

print(q.nodes_to_str())

table = TableLR(g)

table.load('test')

p = Parser(g, table)

q = p.parse(p.str_to_tokens('n + n * n'))

print(q.error)

def dfs(t):
    print(t.token)
    for i in t.children:
        dfs(i)


# dfs(q.derivation_tree)
