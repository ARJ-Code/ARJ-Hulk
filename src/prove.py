from compiler_tools.automaton import Automaton,pattern_to_automaton

a=pattern_to_automaton('a')
b=pattern_to_automaton('b')

a.to_dfa()

a.concat(b)