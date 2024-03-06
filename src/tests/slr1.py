from parser.automatonSLR1 import AutomatonSLR1
from parser.grammar import Grammar


def test():
    g = Grammar()

    g.add_main("S")
    g.add_production("S", ["E"])
    g.add_production("E", ["T + E", "T"])
    g.add_production("T", ["F * T", "F"])
    g.add_production("F", ["F ^ G", "G"])
    g.add_production("G", ["n", "( E )"])

    g1 = Grammar()

    g1.add_main("S")
    g1.add_production("S", ["E"])
    g1.add_production("F", ["( E )", "n"])
    g1.add_production("E", ["A = A", "i"])
    g1.add_production("A", ["i + A", "i"])

    q = AutomatonSLR1('test1_slr1', g)
    q1 = AutomatonSLR1('test2_slr1', g1)

    assert q.ok
    assert not q1.ok
