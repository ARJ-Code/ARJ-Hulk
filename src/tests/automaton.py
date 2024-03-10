from compiler_tools.automaton import Automaton,pattern_to_automaton

def test():
    a = pattern_to_automaton('a')
    assert isinstance(a, Automaton)
    assert len(a.states) == 2
    assert len(a.initial_state.transitions) == 1
    assert 'a' in a.initial_state.transitions
    assert a.initial_state.transitions['a'] == a.final_states[0]

    assert a.match('a')
    assert not a.match('aa')

    b=pattern_to_automaton('b')
    c=pattern_to_automaton('c')

    a.join(b)

    assert a.match('a')
    assert a.to_dfa().match('a')

    a.concat(c)
    a.to_dfa()

    assert a.match('ac')