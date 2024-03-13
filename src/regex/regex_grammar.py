from compiler_tools.grammar import GrammarToken
from compiler_tools.attributed_grammar import AttributedGrammar,AttributedRule
from .regex_ast import *
from .regex_core import RegexToken

regex_special_tokens = ['?', '+', '*', '^',
                        '$', '[', ']', '(', ')', '{', '}', '.', '|', '-']

regex_grammar = AttributedGrammar()

r0 = AttributedRule[RegexAst,RegexToken](lambda _, s: s[1])

r1 = AttributedRule[RegexAst, RegexToken](lambda _, s: RegexOr(s[1], s[3]))
r2 = AttributedRule[RegexAst, RegexToken](lambda _, s: s[1])

r3 = AttributedRule[RegexAst, RegexToken](lambda _, s: RegexConcat(s[1], s[2]))
r4 = AttributedRule[RegexAst, RegexToken](lambda _, s: s[1])

r5 = AttributedRule[RegexAst, RegexToken](
    lambda _, s: s[4], [(3, lambda _, s: s[2])])
r6 = AttributedRule[RegexAst, RegexToken](
    lambda _, s: s[2], [(1, lambda _, s: s[1])])

r7 = AttributedRule[RegexAst, RegexToken](lambda h, _: RegexQuestion(h[0]))
r8 = AttributedRule[RegexAst, RegexToken](lambda h, _: RegexOneAndMany(h[0]))
r9 = AttributedRule[RegexAst, RegexToken](lambda h, _: RegexMany(h[0]))
r10 = AttributedRule[RegexAst, RegexToken](lambda h, _: h[0])

r11 = AttributedRule[RegexAst, RegexToken](lambda _, s: RegexChar(s[1]  .value))
r12 = AttributedRule[RegexAst, RegexToken](lambda _, s: s[2])
r13 = AttributedRule[RegexAst, RegexToken](lambda _, s: RegexAnyChar())

r14 = AttributedRule[RegexAst, RegexToken](lambda _, s: RegexNot(s[2]))
r15 = AttributedRule[RegexAst, RegexToken](lambda _, s: s[1])

r16 = AttributedRule[RegexAst, RegexToken](lambda _, s: RegexOr(s[1], s[2]))
r17 = AttributedRule[RegexAst, RegexToken](lambda _, s: s[1])

r18 = AttributedRule[RegexAst, RegexToken](lambda _, s: RegexChar(s[1].value))
r19 = AttributedRule[RegexAst, RegexToken](
    lambda _, s: RegexRank(s[1].value, s[3].value))


regex_grammar.add_main('S')
regex_grammar.add_attributed_production('S', ['E'],[r0])
regex_grammar.add_attributed_production('E', ['A | E', 'A'],[r1,r2])
regex_grammar.add_attributed_production('A', ['F A', 'F'],[r3,r4])
regex_grammar.add_attributed_production('F', ['[ G ] I', 'H I'],[r5,r6])
regex_grammar.add_attributed_production('I', ['?', '+', '*',  ''],[r7,r8,r9,r10])
regex_grammar.add_attributed_production('H', ['ch', '( E )', '.'],[r11,r12,r13])
regex_grammar.add_attributed_production('G', ['^ J', 'J'],[r14,r15])
regex_grammar.add_attributed_production('J', ['K J', 'K'],[r16,r17])
regex_grammar.add_attributed_production('K', ['ch', 'ch - ch'],[r18,r19])


def regex_to_grammar(token: RegexToken) -> GrammarToken:
    if token.is_special:
        return [t for t in regex_grammar.terminals if t.value == token.value][0]

    return [t for t in regex_grammar.terminals if t.value == 'ch'][0]
