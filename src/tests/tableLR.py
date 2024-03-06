from parser.parser import Parser
from parser.tableLR import TableLR
from parser.grammar import Grammar


def test():
    g = Grammar()

    g.add_main("S")
    g.add_production("S", ["E"])
    g.add_production("E", ["T + E", "T"])
    g.add_production("T", ["F * T", "F"])
    g.add_production("F", ["F ^ G", "G"])
    g.add_production("G", ["n", "( E )"])

    table = TableLR(g)

    table.load('test1_slr1')

    p = Parser(g, table)

    q = p.parse(p.str_to_tokens('n ^ n * ( n + n )'))
    q1 = p.parse(p.str_to_tokens('n n * ( n + n )'))

    assert q.ok
    assert not q1.ok
    assert q1.error == 1
