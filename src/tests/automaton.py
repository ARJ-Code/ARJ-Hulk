from compiler_tools.automaton import Automaton, pattern_to_automaton


def test():
    a = pattern_to_automaton('a')
    assert isinstance(a, Automaton)
    assert len(a.states) == 3
    assert len(a.initial_state.transitions) == 1
    assert 'a' in a.initial_state.transitions
    assert a.initial_state.transitions['a'] == a.final_states[0]

    assert a.match('a')
    assert not a.match('q')
    assert not a.match('aa')

    b = pattern_to_automaton('b')
    c = pattern_to_automaton('c')

    a.join(b)

    assert a.match('b')
    assert a.to_dfa().match('a')

    a.concat(c)

    assert not a.match('ad')

    a.many()
    a = a.to_dfa()

    assert a.match('acacbc')
    assert a.match('')

    a.complement()

    assert a.match('1222')
    assert a.match('acdc')
    assert not a.match('acbc')
    assert not a.match('')

    a.complement()
    a = a.to_dfa()

    assert a.match('ac')
    assert not a.match('233')

    w = pattern_to_automaton('w')
    q = pattern_to_automaton('q')

    w.join(q)
    w.intersection(q)

    assert w.match('q')
    assert not q.match('w')

    x = pattern_to_automaton('x')
    y = pattern_to_automaton('y')

    x.intersection(y)

    for l in ['a', 'b', 'c', 'd']:
        assert not x.match(l)

    m= pattern_to_automaton('m')
    n=m.copy()
    n.complement()

    m.intersection(n)

    assert not m.match('m')
    assert not m.match('')