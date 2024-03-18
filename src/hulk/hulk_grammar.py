from compiler_tools.attributed_grammar import AttributedGrammar, AttributedRule
from compiler_tools.lexer import LexerToken
from hulk.hulk_ast import *
# from hulk.hulk_atributed_rules import *

hulk_grammar = AttributedGrammar()

hulk_grammar.add_main('P')

# program productions
r0 = AttributedRule[ASTNode, LexerToken](lambda h, s: ProgramNode(s[1], s[2], s[4]))
r1 = AttributedRule[ASTNode, LexerToken](lambda h, s: ProgramNode(s[1], s[2], s[3]))
hulk_grammar.add_attributed_production('P', ['I2s EB ; I2s', 'I2s EB I2s'], [r0, r1])


# instructions productions
r2 = AttributedRule[ASTNode, LexerToken](lambda h, s: s[1] + [s[2]])
r3 = AttributedRule[ASTNode, LexerToken](lambda h, s: EOFNode())
hulk_grammar.add_attributed_production('I2s', ['I2s I', ''], [r2, r3])

r4 = AttributedRule[ASTNode, LexerToken](lambda _, s: s[1])
hulk_grammar.add_attributed_production('I', ['C', 'F', 'Pr'], [r4, r4, r4])


# expression productions
hulk_grammar.add_attributed_production('EB', ['E', 'B'], [r4, r4])

r5 = AttributedRule[ASTNode, LexerToken](lambda _, s: s[2])
hulk_grammar.add_attributed_production('B', ['{ I1s }'], [r5])

hulk_grammar.add_attributed_production('I1s', ['I1s E ;', 'E ;'], [r2, r4])

hulk_grammar.add_attributed_production('E', ['Es', 'El', 'Eif', 'Ew', 'Ef', 'Eas', 'Ear'], [r4, r4, r4, r4, r4, r4, r4])


# string expression productions
r6 = AttributedRule[ASTNode, LexerToken](lambda h,s: StringBinaryNode(s[1],s[3], StringOperator.CONCAT))
r7 = AttributedRule[ASTNode, LexerToken](lambda h,s: StringBinaryNode(s[1],s[3], StringOperator.SPACED_CONCAT))
hulk_grammar.add_attributed_production('Es', ['Es @ Ts', 'Es @@ Ts', 'Ts'], [r6, r7, r4])

hulk_grammar.add_attributed_production('Ts', ['Eb'], [r4])


# boolean expression productions
r8 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3], BooleanOperator.OR))
hulk_grammar.add_attributed_production('Eb', ['Eb | Fb', 'Tb'], [r8, r4])

r9 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3], BooleanOperator.AND))
hulk_grammar.add_attributed_production('Tb', ['Tb & Fb', 'Fb'], [r9, r4])

r10 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanUnaryNode(s[2], BooleanOperator.NOT))
hulk_grammar.add_attributed_production('Fb', ['! Cb', 'Cb'], [r10, r4])

r11 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.EQ))
r12 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.LT))
r13 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.GT))
r14 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.GTE))
r15 = AttributedRule[ASTNode, LexerToken](lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.LTE))
hulk_grammar.add_attributed_production(
    'Cb', ['Gb == Gb', 'Gb < Gb', 'Gb > Gb', 'Gb >= Gb', 'Gb <= Gb', 'Gb'], [r11, r12, r13, r14, r15, r4])

hulk_grammar.add_attributed_production('Gb', ['Ea'], [r4])


# arithmetic expression productions
r16 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicBinaryNode(s[1],s[3],AritmethicOperator.ADD))
r17 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicBinaryNode(s[1],s[3],AritmethicOperator.SUB))
hulk_grammar.add_attributed_production('Ea', ['Ea + Ta', 'Ea - Ta', 'Ta'], [r16, r17, r4])

r18 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicBinaryNode(s[1],s[3],AritmethicOperator.MUL))
r19 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicBinaryNode(s[1],s[3],AritmethicOperator.DIV))
hulk_grammar.add_attributed_production('Ta', ['Ta * Fa', 'Ta / Fa', 'Fa'], [r18, r19, r4])

r20 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicBinaryNode(s[1],s[3],AritmethicOperator.POW))
hulk_grammar.add_attributed_production('Fa', ['Ga ^ Fa', 'Ga'], [r20, r4])

r21 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicUnaryNode(s[2], AritmethicOperator.ADD))
r22 = AttributedRule[ASTNode, LexerToken](lambda h,s: AritmethicUnaryNode(s[2], AritmethicOperator.SUB))
hulk_grammar.add_attributed_production('Ga', ['+ Oa', '- Oa', 'Oa'], [r21, r22, r4])

hulk_grammar.add_attributed_production('Oa', ['W'], [r4])

r23 = AttributedRule[ASTNode, LexerToken](lambda h,s: ConstantNode(s[1], ConstantTypes.NUMBER))
r24 = AttributedRule[ASTNode, LexerToken](lambda h,s: ConstantNode(s[1], ConstantTypes.BOOLEAN))
r25 = AttributedRule[ASTNode, LexerToken](lambda h,s: ConstantNode(s[1], ConstantTypes.STRING))
hulk_grammar.add_attributed_production(
    'W', ['Ids', 'num', 'bool', 'str', '( E )', 'Et'], [r4, r23, r24, r25, r5, r4])


# type productions
r26 = AttributedRule[ASTNode, LexerToken](lambda h,s: TypeNode(s[2]))
hulk_grammar.add_attributed_production('T', [': id', ''], [r26, r3])


# declarations productions
r27 = AttributedRule[ASTNode, LexerToken](lambda h,s: DeclarationNode(s[1], s[2], s[4]))
hulk_grammar.add_attributed_production('Sl', ['id T = E'], [r27])

r28 = AttributedRule[ASTNode, LexerToken](lambda h,s: AssignmentNode(s[1], s[3]))
hulk_grammar.add_attributed_production('Eas', ['Ids := E'], [r28])


# let productions
r29 = AttributedRule[ASTNode, LexerToken](lambda h,s: LetNode(s[2], s[4]))
hulk_grammar.add_attributed_production('El', ['let As in EB'], [r29])

r30 = AttributedRule[ASTNode, LexerToken](lambda h,s: s[1] + [s[3]])
hulk_grammar.add_attributed_production('As', ['As , Sl', 'Sl'], [r30, r4])


# if productions
r31 = AttributedRule[ASTNode, LexerToken](lambda h,s: IfNode(s[3], s[5], s[6], s[8]))
hulk_grammar.add_attributed_production(
    'Eif', ['if ( Eb ) EB Eelifs else EB'], [])

hulk_grammar.add_attributed_production('Eelifs', ['Eelifs Eelif', ''], [r2, r3])

r32 = AttributedRule[ASTNode, LexerToken](lambda h,s: ElifNode(s[3], s[5]))
hulk_grammar.add_attributed_production('Eelif', ['elif ( Eb ) EB'], [r32])


# while productions
r33 = AttributedRule[ASTNode, LexerToken](lambda h,s: WhileNode(s[3], s[5]))
hulk_grammar.add_attributed_production('Ew', ['while ( Eb ) EB'], [r33])


# for productions
r34 = AttributedRule[ASTNode, LexerToken](lambda h,s: ForNode(s[3], s[5], s[7]))
hulk_grammar.add_attributed_production('Ef', ['for ( id in E ) EB'], [r34])


# function call productions
r35 = AttributedRule[ASTNode, LexerToken](lambda h,s: FunctionCallNode(s[1], s[3]))
hulk_grammar.add_attributed_production('Ec', ['id ( C1 )'], [r35])

hulk_grammar.add_attributed_production('C1', ['C2', ''], [r4, r3])

hulk_grammar.add_attributed_production('C2', ['E , C2', 'E'], [r30, r4])


# variable productions
r36 = AttributedRule[ASTNode, LexerToken](lambda h,s: InstancePropertyNode(s[1], s[3]))
hulk_grammar.add_attributed_production('Ids', ['Ids . Q', 'Q'], [r36, r4])

hulk_grammar.add_attributed_production('Q', ['id', 'Ec', 'Ac'], [r4, r4, r4])


# function productions
r37 = AttributedRule[ASTNode, LexerToken](lambda h,s: FunctionDeclarationNode(s[2], s[4], s[6], s[7]))
hulk_grammar.add_attributed_production('F', ['function id ( D1 ) T FB'], [r37])

hulk_grammar.add_attributed_production('FB', ['B', '=> E ;'], [r4, r5])

hulk_grammar.add_attributed_production('D1', ['D2', ''], [r4, r3])

r38 = AttributedRule[ASTNode, LexerToken](lambda h,s: [s[1]] + s[3])
hulk_grammar.add_attributed_production('D2', ['D3 , D2', 'D3'], [r38, r4])

r39 = AttributedRule[ASTNode, LexerToken](lambda h,s: TypedParameterNode(s[1], s[2]))
hulk_grammar.add_attributed_production('D3', ['id T'], [r39])


# class productions
r40 = AttributedRule[ASTNode, LexerToken](lambda h,s: ClassTypeNode(s[2]))
r41 = AttributedRule[ASTNode, LexerToken](lambda h,s: ClassTypeParametedNode(s[2], s[4]))
hulk_grammar.add_attributed_production('Hc', ['type id', 'type id ( D2 )'], [r40, r41])

r42 = AttributedRule[ASTNode, LexerToken](lambda h,s: InheritanceNode(s[2]))
r43 = AttributedRule[ASTNode, LexerToken](lambda h,s: InheritanceParametedNode(s[2], s[4]))
hulk_grammar.add_attributed_production('Hih', ['inherits id', 'inherits id ( C2 )', ''], [r42, r43, r3])

r44 = AttributedRule[ASTNode, LexerToken](lambda h,s: ClassDeclarationNode(s[1], s[2], s[4]))
hulk_grammar.add_attributed_production('C', ['Hc Hih { CB }'], [r44])

hulk_grammar.add_attributed_production('CB', ['CB IC', ''], [r2, r3])

r45 = AttributedRule[ASTNode, LexerToken](lambda h,s: ClassPropertyNode(s[1], s[2], s[4]))
r46 = AttributedRule[ASTNode, LexerToken](lambda h,s: ClassFunctionNode(s[1], s[3], s[5], s[6]))
hulk_grammar.add_attributed_production('IC', ['id T = E ;', 'id ( D1 ) T FB'], [r45, r46])


# type inference productions
r47 = AttributedRule[ASTNode, LexerToken](lambda h,s: IsNode(s[1], s[3]))
r48 = AttributedRule[ASTNode, LexerToken](lambda h,s: AsNode(s[1], s[3]))
r49 = AttributedRule[ASTNode, LexerToken](lambda h,s: NewNode(s[2]))
hulk_grammar.add_attributed_production('Et', ['Ids is id', 'Ids as id', 'new Ec'], [r47, r48, r49])


# array productions
hulk_grammar.add_attributed_production('Ear', ['[ X1 ]'], [])
hulk_grammar.add_attributed_production('X1', ['E || id in E', 'X2', ''], [])
hulk_grammar.add_attributed_production('X2', ['X2 , E', 'E'], [])


# array indexation productions
hulk_grammar.add_attributed_production('Ac', ['id Y1'], [])
hulk_grammar.add_attributed_production('Y1', ['Y1 [ E ]', '[ E ]'], [])


# protocol productions
hulk_grammar.add_attributed_production('Pr', ['protocol id { PB }', 'protocol id extends id { PB }'], [])
hulk_grammar.add_attributed_production('PB', ['PB id ( D1 ) T ;', 'id ( D1 ) T ;'], [])
