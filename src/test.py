from hulk_parser.grammar import Grammar

g=Grammar()

g.add_main("S")
g.add_production("S", ["A B","S B","EOF"])
g.calculate_first()
g.calculate_follow()

for i in g.follows:
    for j in g.follows[i]:
        print(i, j)