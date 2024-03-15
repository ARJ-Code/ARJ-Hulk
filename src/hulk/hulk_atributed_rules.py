from compiler_tools.grammar import GrammarToken
from compiler_tools.attributed_grammar import AttributedGrammar, AttributedRule
from compiler_tools.lexer import LexerToken
from hulk.hulk_ast import *

# generic rules
rs1 = AttributedRule[ASTNode, LexerToken](lambda _, s: s[1])
rs2 = AttributedRule[ASTNode, LexerToken](lambda _, s: s[2])

# hulk rules

#great rules
r0 = rs1
r1 = AttributedRule[ASTNode, LexerToken](lambda h,s: ListNode(s[1],s[2]))
r2 = rs1
r3 = rs1
r4 = rs1

#instructions1 rules
r5 = rs1
r6 = rs1
r7 = None
r8 = rs1
r9 = AttributedRule[ASTNode, LexerToken](lambda h,s: ListNode(s[1],s[2]))
r10 = rs1

#instructions block rules
r11 = rs1
r12 = rs1
r13 = rs1
r14 = rs1
r15 = rs1
r16 = rs1
r17 = rs1
r18 = rs2

#instructions2 rules
r19 = rs1
r20 = rs1
r21 = rs1

# expression rules
r22 = rs1
r23 = rs1
r24 = rs1
r25 = rs1
r26 = rs1
r27 = rs1
r28 = rs1

# string expression rules
r29 = AttributedRule[ASTNode, LexerToken](lambda h,s: StringExpressionNode(s[1],s[3], StringOperator.CONCAT))
r30 = AttributedRule[ASTNode, LexerToken](lambda h,s: StringExpressionNode(s[1],s[3], StringOperator.SPACED_CONCAT))
r31 = rs1
r32 = rs1

# boolean expression rules
r33 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3], BooleanOperator.OR))
r34 = rs1
r35 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3], BooleanOperator.AND))
r36 = rs1
r37 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanUnaryNode(s[2], BooleanOperator.NOT))
r38 = rs1
r39 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.EQ))
r40 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.LT))
r41 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.GT))
r42 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.GTE))
r43 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.LTE))
r44 = rs1
r45 = rs1

# aritmetic expression rules
r46 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmeticBinaryNode(s[1],s[3],AritmeticOperator.ADD))
r47 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmeticBinaryNode(s[1],s[3],AritmeticOperator.SUB))
r48 = rs1
r49 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmeticBinaryNode(s[1],s[3],AritmeticOperator.MUL))
r50 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmeticBinaryNode(s[1],s[3],AritmeticOperator.DIV))
r51 = rs1
r52 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmeticBinaryNode(s[1],s[3],AritmeticOperator.POW))
r53 = rs1
r54 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmeticUnaryNode(s[2], AritmeticOperator.ADD))
r55 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmeticUnaryNode(s[2], AritmeticOperator.SUB))
r56 = rs1
r57 = rs1

# atomic rules
r58 = rs1
r59 = AttributedRule[ASTNode, LexerToken](lambda h,s: ConstantNode(s[1], ConstantTypes.NUMBER))
r60 = AttributedRule[ASTNode, LexerToken](lambda h,s: ConstantNode(s[1], ConstantTypes.BOOLEAN))
r61 = AttributedRule[ASTNode, LexerToken](lambda h,s: ConstantNode(s[1], ConstantTypes.STRING))
r62 = rs2
r63 = rs1

# type rules
r64 = AttributedRule[ASTNode, LexerToken](lambda h,s: TypeNode(s[2]))
r65 = None

# let expression rules
r66 = AttributedRule[ASTNode, LexerToken](lambda h,s: LetExpressionNode(s[2],s[4]))
















