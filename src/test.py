from hulk_parser.grammar import Grammar
from hulk_parser.automatonSLR import AutomatonSLR
from hulk_parser.tableLR import TableLR

g = Grammar()

g.add_main("S")
g.add_production("S", ["E", "EOF"])
g.add_production("E", ["E + T","T"])
g.add_production("T", ["T * F", "F"])
g.add_production("F", ["( E )", "id"])

g1=Grammar()

g1.add_main('S')
g1.add_production('S',['E'])
g1.add_production('E',['A = A','i'])
g1.add_production('A',['i + A','i'])


q = AutomatonSLR('test',g1)
# TableLR(g1).load('test')
# g.calculate_first()

# for i in g.firsts:
#     for j in g.firsts[i]:
#         print(i, j)

# g.calculate_follow()

for a in q.nodes:
    for x in a.items:
        print(str(x.production)+" "+str(x.index))
    print("******")

# for a in q.nodes:
#     for x,y in a.transitions.items():
#         print(a.ind, y, str(x))