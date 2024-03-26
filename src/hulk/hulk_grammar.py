from compiler_tools.attributed_grammar import AttributedGrammar, AttributedRule
from compiler_tools.lexer import LexerToken
from hulk.hulk_ast import *

hulk_grammar = AttributedGrammar()

hulk_grammar.add_main('P')

r00 = AttributedRule[ASTNode, LexerToken](lambda _, s: [])
r01 = AttributedRule[ASTNode, LexerToken](lambda _, s: [s[1]])
r02 = AttributedRule[ASTNode, LexerToken](lambda _, s: [s[2]])

# program productions
r0 = AttributedRule[ASTNode, LexerToken](lambda _, s: s[1])
hulk_grammar.add_attributed_production('P', ['P1'], [r0])

r1 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ProgramNode(s[1], s[2], s[4]))
r2 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ProgramNode(s[1], s[2], s[3]))
hulk_grammar.add_attributed_production(
    'P1', ['I2s EB ; I2s', 'I2s EB I2s'], [r1, r2])


# instructions productions
r3 = AttributedRule[ASTNode, LexerToken](lambda h, s: s[1] + [s[2]])
r4 = AttributedRule[ASTNode, LexerToken](lambda h, s: EOFNode())
hulk_grammar.add_attributed_production('I2s', ['I2s I', ''], [r3, r00])


hulk_grammar.add_attributed_production('I', ['C', 'F', 'Pr'], [r0, r0, r0])


# expression productions
hulk_grammar.add_attributed_production('EB', ['E', 'B'], [r0, r0])

r5 = AttributedRule[ASTNode, LexerToken](lambda _, s: s[2])
r51 = AttributedRule[ASTNode, LexerToken](lambda _, s: ExpressionBlock(s[2]))
hulk_grammar.add_attributed_production('B', ['{ I1s }'], [r51])

hulk_grammar.add_attributed_production('I1s', ['I1s E ;', 'E ;'], [r3, r01])

hulk_grammar.add_attributed_production(
    'E', ['Es', 'El', 'Eif', 'Ew', 'Ef', 'Eas', 'Ear'], [r0, r0, r0, r0, r0, r0, r0])


# string expression productions
r6 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: StringBinaryNode(s[1], s[3], StringOperator.CONCAT))
r7 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: StringBinaryNode(s[1], s[3], StringOperator.SPACED_CONCAT))
hulk_grammar.add_attributed_production(
    'Es', ['Es @ Ts', 'Es @@ Ts', 'Ts'], [r6, r7, r0])

hulk_grammar.add_attributed_production('Ts', ['Eb'], [r0])


# boolean expression productions
r8 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.OR))
hulk_grammar.add_attributed_production('Eb', ['Eb | Fb', 'Tb'], [r8, r0])

r9 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.AND))
hulk_grammar.add_attributed_production('Tb', ['Tb & Fb', 'Fb'], [r9, r0])

r10 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanUnaryNode(s[2], BooleanOperator.NOT))
hulk_grammar.add_attributed_production('Fb', ['! Cb', 'Cb'], [r10, r0])

r11 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.EQ))
neq = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.NEQ))
r12 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.LT))
r13 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.GT))
r14 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.GTE))
r15 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.LTE))
hulk_grammar.add_attributed_production(
    'Cb', ['Gb == Gb', 'Gb != Gb', 'Gb < Gb', 'Gb > Gb', 'Gb >= Gb', 'Gb <= Gb', 'Gb'], [r11, neq, r12, r13, r14, r15, r0])

hulk_grammar.add_attributed_production('Gb', ['Ea'], [r0])


# arithmetic expression productions
r16 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticBinaryNode(s[1], s[3], ArithmeticOperator.ADD))
r17 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticBinaryNode(s[1], s[3], ArithmeticOperator.SUB))
hulk_grammar.add_attributed_production(
    'Ea', ['Ea + Ta', 'Ea - Ta', 'Ta'], [r16, r17, r0])

r18 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticBinaryNode(s[1], s[3], ArithmeticOperator.MUL))
r19 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticBinaryNode(s[1], s[3], ArithmeticOperator.DIV))
hulk_grammar.add_attributed_production(
    'Ta', ['Ta * Fa', 'Ta / Fa', 'Fa'], [r18, r19, r0])

r20 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticBinaryNode(s[1], s[3], ArithmeticOperator.POW))
hulk_grammar.add_attributed_production('Fa', ['Ga ^ Fa', 'Ga'], [r20, r0])

r21 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticUnaryNode(s[2], ArithmeticOperator.ADD))
r22 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticUnaryNode(s[2], ArithmeticOperator.SUB))
hulk_grammar.add_attributed_production(
    'Ga', ['+ Oa', '- Oa', 'Oa'], [r21, r22, r0])

hulk_grammar.add_attributed_production('Oa', ['W'], [r0])

r23 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ConstantNode(s[1], ConstantTypes.NUMBER))
r24 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ConstantNode(s[1], ConstantTypes.BOOLEAN))
r25 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ConstantNode(s[1], ConstantTypes.STRING))
r231 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: AtomicNode(s[1]))
r232 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: InstancePropertyNode(s[1], s[3]))
r233 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: InstanceFunctionNode(s[1], s[3]))
r234 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: InstanceFunctionNode(AtomicNode(s[1]), s[3]))


hulk_grammar.add_attributed_production(
    'Epc', ['Epc . Ec', 'Ec . Ec', 'id . Ec'], [r233, r233, r234])

hulk_grammar.add_attributed_production(
    'W', ['id', 'id . id', 'num', 'bool', 'str', '( E )', 'Et', 'Ec', 'Epc', 'Ac'], [r231, r232, r23, r24, r25, r5, r0, r0, r0, r0])


# type productions
eof_type = AttributedRule[ASTNode, LexerToken](lambda h, s: EOFTypeNode())
hulk_grammar.add_attributed_production('Tno', [': T', ''], [r02, eof_type])

hulk_grammar.add_attributed_production('To', [': T'], [r02])

r26 = AttributedRule[ASTNode, LexerToken](lambda h, s: TypeNode(s[1]))
vt = AttributedRule[AsNode, LexerToken](
    lambda h, s: VectorTypeNode(s[2], None))
vtd = AttributedRule[AsNode, LexerToken](
    lambda h, s: VectorTypeNode(s[2], s[4]))
hulk_grammar.add_attributed_production(
    'T', ['id', '[ id ]', '[ id , num ]'], [r26, vt, vtd])


# declarations productions
r27 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: DeclarationNode(s[1], s[2], s[4]))
hulk_grammar.add_attributed_production('Sl', ['id Tno = E'], [r27])

r28 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: AssignmentNode(s[1], s[3]))

r281 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: AssignmentArrayNode(s[1], s[3]))

r282 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: AssignmentPropertyNode(s[1], s[3], s[5]))

hulk_grammar.add_attributed_production(
    'Eas', ['id := E', 'Ac := E', 'id . id := E'], [r28, r281, r282])


# let productions
r29 = AttributedRule[ASTNode, LexerToken](lambda h, s: LetNode(s[2], s[4]))
hulk_grammar.add_attributed_production('El', ['let As in EB'], [r29])

r30 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: [s[1]] + s[3])
hulk_grammar.add_attributed_production('As', ['Sl , As', 'Sl'], [r30, r01])


# if productions
r31 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: IfNode(s[3], s[5], s[6], s[8]))
hulk_grammar.add_attributed_production(
    'Eif', ['if ( Eb ) EB Eelifs else EB'], [r31])

hulk_grammar.add_attributed_production(
    'Eelifs', ['Eelifs Eelif', ''], [r3, r00])

r32 = AttributedRule[ASTNode, LexerToken](lambda h, s: ElifNode(s[3], s[5]))
hulk_grammar.add_attributed_production('Eelif', ['elif ( Eb ) EB'], [r32])


# while productions
r33 = AttributedRule[ASTNode, LexerToken](lambda h, s: WhileNode(s[3], s[5]))
hulk_grammar.add_attributed_production('Ew', ['while ( Eb ) EB'], [r33])


# for productions
r34 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ForNode(s[3], s[5], s[7]))
hulk_grammar.add_attributed_production('Ef', ['for ( id in E ) EB'], [r34])


# function call productions
r35 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ExpressionCallNode(s[1], s[3]))
hulk_grammar.add_attributed_production('Ec', ['id ( C1 )'], [r35])

hulk_grammar.add_attributed_production('C1', ['C2', ''], [r0, r00])

hulk_grammar.add_attributed_production('C2', ['E , C2', 'E'], [r30, r01])

# function productions
r37 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: FunctionDeclarationNode(s[2], s[4], s[6], s[7]))
hulk_grammar.add_attributed_production(
    'F', ['function id ( D1 ) To FB'], [r37])

hulk_grammar.add_attributed_production('FB', ['B', '=> E ;'], [r0, r5])

hulk_grammar.add_attributed_production('D1', ['D2', ''], [r0, r00])

hulk_grammar.add_attributed_production('D2', ['D3 , D2', 'D3'], [r30, r01])

r39 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: TypedParameterNode(s[1], s[2]))
hulk_grammar.add_attributed_production('D3', ['id To'], [r39])


# class productions
r40 = AttributedRule[ASTNode, LexerToken](lambda h, s: ClassTypeNode(s[2]))
r41 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ClassTypeParameterNode(s[2], s[4]))
hulk_grammar.add_attributed_production(
    'Hc', ['type id', 'type id ( D2 )'], [r40, r41])

r42 = AttributedRule[ASTNode, LexerToken](lambda h, s: InheritanceNode(s[2]))
r43 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: InheritanceParameterNode(s[2], s[4]))
hulk_grammar.add_attributed_production(
    'Hih', ['inherits id', 'inherits id ( C2 )', ''], [r42, r43, eof_type])

r44 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ClassDeclarationNode(s[1], s[2], s[4]))
hulk_grammar.add_attributed_production('C', ['Hc Hih { CB }'], [r44])

hulk_grammar.add_attributed_production('CB', ['CB IC', ''], [r3, r00])

r45 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ClassPropertyNode(s[1], s[2], s[4]))
r46 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ClassFunctionNode(s[1], s[3], s[5], s[6]))
hulk_grammar.add_attributed_production(
    'IC', ['id Tno = E ;', 'id ( D1 ) To FB'], [r45, r46])


# type inference productions
r47 = AttributedRule[ASTNode, LexerToken](lambda h, s: IsNode(s[1], s[3]))
r48 = AttributedRule[ASTNode, LexerToken](lambda h, s: AsNode(s[1], s[3]))
r49 = AttributedRule[ASTNode, LexerToken](lambda h, s: NewNode(s[2]))
hulk_grammar.add_attributed_production(
    'Et', ['W is id', 'W as id', 'new Ec'], [r47, r48, r49])


# vector productions
hulk_grammar.add_attributed_production('Ear', ['[ X1 ]'], [r5])

r50 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ImplicitArrayDeclarationNode(s[1], s[3], s[5]))
r51 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ExplicitArrayDeclarationNode(s[1]))
r512 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ExplicitArrayDeclarationNode([]))
hulk_grammar.add_attributed_production(
    'X1', ['E || id in E', 'X2', ''], [r50, r51, r512])

r52 = AttributedRule[ASTNode, LexerToken](lambda h, s: s[1] + [s[3]])
hulk_grammar.add_attributed_production('X2', ['X2 , E', 'E'], [r52, r01])


# vector indexation productions
r53 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArrayCallNode(AtomicNode(s[1]), s[3]))

r531 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArrayCallNode(s[1], s[3]))
hulk_grammar.add_attributed_production(
    'Ac', ['id [ E ]', 'Ec [ E ]', 'Ac [ E ]', 'Epc [ E ]'], [r53, r531, r531, r531])


# protocol productions
r54 = AttributedRule[ASTNode, LexerToken](lambda h, s: ProtocolTypeNode(s[2]))
hulk_grammar.add_attributed_production('PT', ['protocol id'], [r54])

r55 = AttributedRule[ASTNode, LexerToken](lambda h, s: ExtensionNode(s[2]))
eof_extension = AttributedRule[ASTNode, LexerToken](lambda h, s: EOFExtensionNode())
hulk_grammar.add_attributed_production('Prex', ['extends id', ''], [r55, eof_extension])

r56 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ProtocolDeclarationNode(s[1], s[2], s[4]))
hulk_grammar.add_attributed_production('Pr', ['PT Prex { PB }'], [r56])

hulk_grammar.add_attributed_production('PB', ['PB PF', 'PF'], [r3, r01])

r57 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ProtocolFunctionNode(s[1], s[3], s[5]))
hulk_grammar.add_attributed_production('PF', ['id ( D1 ) To ;'], [r57])
