from compiler_tools.grammar import GrammarToken
from compiler_tools.attributed_grammar import AttributedGrammar, AttributedRule
from compiler_tools.lexer import LexerToken
from hulk.hulk_ast import *

# generic rules
rs1 = AttributedRule[ASTNode, LexerToken](lambda _, s: s[1])
rs2 = AttributedRule[ASTNode, LexerToken](lambda _, s: s[2])

# hulk rules


r0 = rs1
rs2 = AttributedRule[ASTNode, LexerToken](lambda h,s: ListNode(s[1],s[2]))
rs3 = rs1
rs4 = rs1
rs5 = rs1
rs6 = rs1
rs7 = rs1



