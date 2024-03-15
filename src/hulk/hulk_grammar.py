from compiler_tools.attributed_grammar import AttributedGrammar, AttributedRule
from hulk.hulk_ast import *

hulk_grammar = AttributedGrammar()

hulk_grammar.add_main('P')

hulk_grammar.add_attributed_production('P', ['Is'], [], [lambda h,s: s[1]])
hulk_grammar.add_attributed_production('Is', ['Is I', 'I'], [], [lambda h,s: ListNode(s[1],s[2]), lambda h,s: s[1]])
hulk_grammar.add_attributed_production('I', ['I1', 'I2'], [], [lambda h,s: s[1], lambda h,s: s[1]])

hulk_grammar.add_attributed_production('I1', ['E ;', 'IB', ';', 'Il'], [], [lambda h,s: s[1], lambda h,s: s[1], lambda h,s: None, lambda h,s: s[1]])
hulk_grammar.add_attributed_production('I1s', ['I1s I1', 'I1'], [], [lambda h,s: ListNode(s[1],s[2]), lambda h,s: s[1]])
hulk_grammar.add_attributed_production(
    'IB', ['B', 'Bl', 'Bw', 'Bf', 'Bif'], [], [lambda h,s: s[1],lambda h,s: s[1],lambda h,s: s[1],lambda h,s: s[1],lambda h,s: s[1],])
hulk_grammar.add_attributed_production(
    'IBif', ['B', 'E ;'], [], [lambda h,s: s[1],lambda h,s: s[1]])
hulk_grammar.add_attributed_production('B', ['{ I1s }'], [], [lambda h,s: s[2]])

hulk_grammar.add_attributed_production('I2', ['C', 'F', 'Pr'], [], [lambda h,s: s[1],lambda h,s: s[1],lambda h,s: s[1]])

hulk_grammar.add_attributed_production(
    'E', ['Es', 'El', 'Eif', 'Ew', 'Ef', 'Eas', 'Ear'], [], [lambda h,s: s[1],lambda h,s: s[1],lambda h,s: s[1],lambda h,s: s[1],lambda h,s: s[1],lambda h,s: s[1],lambda h,s: s[1],])

hulk_grammar.add_attributed_production('Es', ['Es @ Ts', 'Es @@ Ts', 'Ts'], [], [lambda h,s: StringExpressionNode(s[1],s[3], StringOperator.CONCAT),lambda h,s: StringExpressionNode(s[1],s[3], StringOperator.SPACED_CONCAT),lambda h,s: s[1]])
hulk_grammar.add_attributed_production('Ts', ['Eb'], [], [lambda h,s: s[1]])

hulk_grammar.add_attributed_production('Eb', ['Eb | Fb', 'Tb'], [], [lambda h,s: BooleanBinaryNode(s[1],s[3], BooleanOperator.OR),lambda h,s: s[1]])
hulk_grammar.add_attributed_production('Tb', ['Tb & Fb', 'Fb'], [], [lambda h,s: BooleanBinaryNode(s[1],s[3], BooleanOperator.AND),lambda h,s: s[1]])
hulk_grammar.add_attributed_production('Fb', ['! Cb', 'Cb'], [], [lambda h,s: BooleanUnaryNode(s[2], BooleanOperator.NOT),lambda h,s: s[1]])
hulk_grammar.add_attributed_production(
    'Cb', ['Gb == Gb', 'Gb < Gb', 'Gb > Gb', 'Gb >= Gb', 'Gb <= Gb', 'Gb'], [], [lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.EQ), lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.LT), lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.GT), lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.GTE), lambda h,s: BooleanBinaryNode(s[1],s[3],BooleanOperator.LTE), lambda h,s: s[1]])
hulk_grammar.add_attributed_production('Gb', ['Ea'], [], [lambda h,s: s[1]])

hulk_grammar.add_attributed_production('Ea', ['Ea + Ta', 'Ea - Ta', 'Ta'], [], [lambda h,s: AritmeticBinaryNode(s[1],s[3],AritmeticOperator.ADD),lambda h,s: AritmeticBinaryNode(s[1],s[3],AritmeticOperator.SUB),lambda h,s: s[1]])
hulk_grammar.add_attributed_production('Ta', ['Ta * Fa', 'Ta / Fa', 'Fa'], [], [lambda h,s: AritmeticBinaryNode(s[1],s[3],AritmeticOperator.MUL),lambda h,s: AritmeticBinaryNode(s[1],s[3],AritmeticOperator.DIV),lambda h,s: s[1]])
hulk_grammar.add_attributed_production('Fa', ['Ga ^ Fa', 'Ga'], [], [lambda h,s: AritmeticBinaryNode(s[1],s[3],AritmeticOperator.POW),lambda h,s: s[1]])
hulk_grammar.add_attributed_production('Ga', ['+ Oa', '- Oa', 'Oa'], [], [lambda h,s: AritmeticUnaryNode(s[2], AritmeticOperator.ADD),lambda h,s: AritmeticUnaryNode(s[2], AritmeticOperator.SUB),lambda h,s: s[1]])
hulk_grammar.add_attributed_production('Oa', ['W'], [], [lambda h,s: s[1]])
hulk_grammar.add_attributed_production(
    'W', ['Ids', 'num', 'bool', 'str', '( E )', 'Et'], [], [lambda h,s : s[1], lambda h,s: ConstantNode(s[1], ConstantTypes.NUMBER), lambda h,s: ConstantNode(s[1], ConstantTypes.BOOLEAN), lambda h,s: ConstantNode(s[1], ConstantTypes.STRING), lambda h,s: s[2], lambda h,s: s[1]])
hulk_grammar.add_attributed_production('T', [': id', ''], [], [lambda h,s: TypeNode(s[2]), lambda h,s: None])

hulk_grammar.add_attributed_production('El', ['let As in E'], [], [lambda h,s: LetExpressionNode(s[2],s[4])])
# cambiar letnode
hulk_grammar.add_attributed_production('As', ['As , Sl', 'Sl'], [])
hulk_grammar.add_attributed_production('Sl', ['id T = E'], [])

hulk_grammar.add_attributed_production('Bl', ['let As in IB'], [],[lambda h,s: LetExpressionNode(s[2],s[4])])

hulk_grammar.add_attributed_production('Il', ['let As ;'], [])

hulk_grammar.add_attributed_production('Eas', ['Ids := E'], [])

hulk_grammar.add_attributed_production('Hif', ['if ( Eb )'], [])
hulk_grammar.add_attributed_production('Helif', ['elfi ( Eb )'], [])

hulk_grammar.add_attributed_production(
    'Eif', ['Hif E Eelifs else E'], [])
hulk_grammar.add_attributed_production('Eelifs', ['Eelif Eelifs', ''], [])
hulk_grammar.add_attributed_production('Eelif', ['Helif E'], [])

hulk_grammar.add_attributed_production(
    'Bif', ['Hif IBif Belifs Belse'], [])
hulk_grammar.add_attributed_production('Belifs', ['Belif Belifs', ''], [])
hulk_grammar.add_attributed_production('Belif', ['Helif IBif'], [])
hulk_grammar.add_attributed_production('Belse', ['else IBif', ''], [])

hulk_grammar.add_attributed_production('Hw', ['while ( Eb )'], [])

hulk_grammar.add_attributed_production('Ew', ['Hw E'], [])

hulk_grammar.add_attributed_production('Bw', ['Hw IB'], [])

hulk_grammar.add_attributed_production(
    'Hf', ['for ( id in E )'], [])

hulk_grammar.add_attributed_production('Ef', ['Hf E'], [])

hulk_grammar.add_attributed_production('Bf', ['Hf IB'], [])

hulk_grammar.add_attributed_production('Ec', ['id ( C1 )'], [])
hulk_grammar.add_attributed_production('C1', ['C2', ''], [])
hulk_grammar.add_attributed_production('C2', ['E , C2', 'E'], [])

hulk_grammar.add_attributed_production('Ids', ['Ids . Q', 'Q'], [])
hulk_grammar.add_attributed_production('Q', ['id', 'Ec', 'Ac'], [])

hulk_grammar.add_attributed_production('Fh', ['id ( D1 )'], [])
hulk_grammar.add_attributed_production('D1', ['', 'D2'], [])
hulk_grammar.add_attributed_production('D2', ['D3 , D2', 'D3'], [])
hulk_grammar.add_attributed_production('D3', ['id T'], [])

hulk_grammar.add_attributed_production('F', ['function Fh T FB'], [])
hulk_grammar.add_attributed_production('FB', ['IB', '=> E ;'], [])

hulk_grammar.add_attributed_production('Hc', ['type Fh', 'type id'], [])
hulk_grammar.add_attributed_production(
    'Hih', ['inherit Ec', 'inherit id', ''], [])

hulk_grammar.add_attributed_production('C', ['Hc Hih { CB }'], [])
hulk_grammar.add_attributed_production('CB', ['CB IC', ''], [])
hulk_grammar.add_attributed_production('IC', ['Cp', 'F'], [])
hulk_grammar.add_attributed_production('Cp', ['id T = E ;'], [])

hulk_grammar.add_attributed_production(
    'Et', ['Ids is id', 'Ids as id', 'new Ec'], [])

hulk_grammar.add_attributed_production('Ear', ['[ X1 ]'], [])
hulk_grammar.add_attributed_production('X1', ['E || id in E', 'X2', ''], [])
hulk_grammar.add_attributed_production('X2', ['X2 , E', 'E'], [])

hulk_grammar.add_attributed_production('Ac', ['id Y1'], [])
hulk_grammar.add_attributed_production('Y1', ['Y1 [ E ]', '[ E ]'], [])

hulk_grammar.add_attributed_production('Pr', ['protocol id Pe { PB }'], [])
hulk_grammar.add_attributed_production('Pe', ['extends id', ''], [])
hulk_grammar.add_attributed_production('PB', ['PB Fh ;', 'Fh ;'], [])
