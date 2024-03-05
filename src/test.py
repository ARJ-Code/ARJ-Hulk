from parser.automatonSLR1 import AutomatonSLR1
from parser.automatonLR1 import AutomatonLR1
from parser.parser import Parser
from parser.tableLR import TableLR
from parser.grammar import Grammar

g = Grammar()

g.add_main("S")
g.add_production("S", ["E"])
g.add_production("E", ["T + E", "T"])
g.add_production("T", ["F * T", "F"])
g.add_production("F", ["F ^ G", "G"])
g.add_production("G", ["n", "( E )"])
# g.add_production("F", ["( E )", "n"])
# g.add_production("E",["A = A","i"])
# g.add_production("A",["i + A","i"])

q = AutomatonSLR1('test', g)
print(q.ok)

print(q.nodes_to_str())

table = TableLR(g)

table.load('test')

p = Parser(g, table)

q = p.parse(p.str_to_tokens('n ^ n * ( n + n )'))

print(q.error)


def dfs(t):
    print(t.token)
    for i in t.children:
        dfs(i)


# dfs(q.derivation_tree)
