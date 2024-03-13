from compiler_tools.attributed_grammar import AttributedGrammar, AttributedRule
from .regex_ast import *


r0 = AttributedRule[RegexAst](lambda _, s: s[1])

r1 = AttributedRule[RegexAst](lambda _, s: RegexOr(s[1], s[3]))
r2 = AttributedRule[RegexAst](lambda _, s: s[1])

r3 = AttributedRule[RegexAst](lambda _, s: RegexConcat(s[1], s[2]))
r4 = AttributedRule[RegexAst](lambda _, s: s[1])

r5 = AttributedRule[RegexAst](
    lambda _, s: s[4], [(3, lambda _, s: s[2])])
r6 = AttributedRule[RegexAst](
    lambda _, s: s[2], [(1, lambda _, s: s[1])])

r7 = AttributedRule[RegexAst](lambda h, _: RegexQuestion(h[0]))
r8 = AttributedRule[RegexAst](lambda h, _: RegexOneAndMany(h[0]))
r9 = AttributedRule[RegexAst](lambda h, _: RegexMany(h[0]))
r10 = AttributedRule[RegexAst](lambda h, _: h[0])

r11 = AttributedRule[RegexAst](lambda _, s: RegexChar(s[1]  .value))
r12 = AttributedRule[RegexAst](lambda _, s: s[2])
r13 = AttributedRule[RegexAst](lambda _, s: RegexAnyChar())

r14 = AttributedRule[RegexAst](lambda _, s: RegexNot(s[2]))
r15 = AttributedRule[RegexAst](lambda _, s: s[1])

r16 = AttributedRule[RegexAst](lambda _, s: RegexOr(s[1], s[2]))
r17 = AttributedRule[RegexAst](lambda _, s: s[1])

r18 = AttributedRule[RegexAst](lambda _, s: RegexChar(s[1].value))
r19 = AttributedRule[RegexAst](
    lambda _, s: RegexRank(s[1].value, s[3].value))

regex_attributed_grammar = AttributedGrammar(
    [r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19])
