from hulk_parser.grammar import Grammar, GrammarToken
from hulk_parser.automatonSLR import AutomatonSLR
from hulk_parser.tableLR import TableLR
from hulk_parser.parser import Parser

g = Grammar()

g.add_main("S")
g.add_production("S", ["E"])
g.add_production("E", ["E + T", "T"])
g.add_production("T", ["T * F", "F"])
g.add_production("F", ["( E )", "n"])

# g1=Grammar()

# g1.add_main('S')
# g1.add_production('S',['E'])
# g1.add_production('E',['A = A','i'])
# g1.add_production('A',['i + A','i'])


q = AutomatonSLR('test',g)

for a in q.nodes:
    for x in a.items:
        print(str(x.production)+" "+str(x.index))
    print("******")


table = TableLR(g)

table.load('test')

p = Parser(g, table)

w=[GrammarToken('n'), GrammarToken('+'),
            GrammarToken('n'), GrammarToken('*'), GrammarToken('n')]
w=[GrammarToken('n'), GrammarToken('+'),
            GrammarToken('n')]
q = p.parse(w)

# print(q.error)

# def dfs(t):
#     print(t.token)
#     for i in t.children:
#         dfs(i)


# dfs(q.derivation_tree)
