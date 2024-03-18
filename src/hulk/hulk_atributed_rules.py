from compiler_tools.attributed_grammar import AttributedRule
from compiler_tools.lexer import LexerToken
from hulk.hulk_ast import *

# generic rules
rs0 = AttributedRule[ASTNode, LexerToken](lambda h,s: EOFNode())
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
r7 = rs0
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
r29 = AttributedRule[ASTNode, LexerToken](lambda h,s: StringBinaryNode(s[1],s[3], StringOperator.CONCAT))
r30 = AttributedRule[ASTNode, LexerToken](lambda h,s: StringBinaryNode(s[1],s[3], StringOperator.SPACED_CONCAT))
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

# aritmethic expression rules
r46 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicBinaryNode(s[1],s[3],AritmethicOperator.ADD))
r47 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicBinaryNode(s[1],s[3],AritmethicOperator.SUB))
r48 = rs1
r49 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicBinaryNode(s[1],s[3],AritmethicOperator.MUL))
r50 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicBinaryNode(s[1],s[3],AritmethicOperator.DIV))
r51 = rs1
r52 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicBinaryNode(s[1],s[3],AritmethicOperator.POW))
r53 = rs1
r54 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicUnaryNode(s[2], AritmethicOperator.ADD))
r55 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicUnaryNode(s[2], AritmethicOperator.SUB))
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
r65 = rs0

# let rules
r66 = AttributedRule[ASTNode, LexerToken](lambda h,s: LetBodyNode(s[2],s[4]))
r67 = AttributedRule[ASTNode, LexerToken](lambda h,s: LetBodyNode(s[2],s[4]))
r68 = AttributedRule[ASTNode, LexerToken](lambda h,s: LetNode(s[2]))
r69 = AttributedRule[ASTNode, LexerToken](lambda h,s: AssignmentNode(s[1],s[3]))

# declarations rules
r70 = AttributedRule[ASTNode, LexerToken](lambda h, s: ListNode(s[1], s[3]))
r71 = AttributedRule[ASTNode, LexerToken](lambda h, s: DeclarationNode(s[1], s[2], s[4]))

# if rules
r72 = AttributedRule[ASTNode, LexerToken](lambda h,s: s[3])
r73 = AttributedRule[ASTNode, LexerToken](lambda h,s: s[3])
r74 = AttributedRule[ASTNode, LexerToken](lambda h,s: IfNode(s[1], s[2], s[3], s[5]))
r75 = AttributedRule[ASTNode, LexerToken](lambda h,s: ListNode(s[1], s[2]))
r76 = rs0
r77 = rs2
r78 = AttributedRule[ASTNode, LexerToken](lambda h,s: IfNode(s[1], s[2], s[3], s[5]))
r79 = AttributedRule[ASTNode, LexerToken](lambda h,s: ListNode(s[1], s[2]))
r80 = rs0
r81 = rs2
r82 = rs2
r83 = rs0

# while rules
r84 = AttributedRule[ASTNode, LexerToken](lambda h,s: s[3])
r85 = AttributedRule[ASTNode, LexerToken](lambda h,s: WhileNode(s[1], s[2]))

# for rules
r86 = AttributedRule[ASTNode, LexerToken](lambda h,s: ForNode(s[3], s[5], s[7]))

# function call rules
r87 = AttributedRule[ASTNode, LexerToken](lambda h,s: FunctionCallNode(s[1], s[3]))
r88 = rs1
r89 = rs0
r90 = AttributedRule[ASTNode, LexerToken](lambda h,s: [s[1]] + s[3])
r91 = rs1

# variable rules
r92 = AttributedRule[ASTNode, LexerToken](lambda h,s: AttributedNode(s[1], s[3]))
r93 = rs1
r94 = rs1
r95 = rs1
r96 = rs1