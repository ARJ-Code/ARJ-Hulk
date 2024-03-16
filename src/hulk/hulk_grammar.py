from compiler_tools.attributed_grammar import AttributedGrammar, AttributedRule
from hulk.hulk_ast import *
from hulk.hulk_atributed_rules import *

hulk_grammar = AttributedGrammar()

hulk_grammar.add_main('P')

# program productions
hulk_grammar.add_attributed_production('P', ['Is'], [r0])

# instruction productions
hulk_grammar.add_attributed_production('Is', ['Is I', 'I'], [r1,r2])
hulk_grammar.add_attributed_production('I', ['I1', 'I2'], [r3,r4])

# expression productions
hulk_grammar.add_attributed_production('I1', ['E ;', 'IB', ';', 'Il'], [r5,r6,r7,r8])
hulk_grammar.add_attributed_production('I1s', ['I1s I1', 'I1'], [r9,r10])
hulk_grammar.add_attributed_production(
    'IB', ['B', 'Bl', 'Bw', 'Bf', 'Bif'], [r11,r12,r13,r14,r15])
hulk_grammar.add_attributed_production(
    'IBif', ['B', 'E ;'], [r16, r17])
hulk_grammar.add_attributed_production('B', ['{ I1s }'], [r18])

hulk_grammar.add_attributed_production('I2', ['C', 'F', 'Pr'], [r19,r20,r21])

hulk_grammar.add_attributed_production(
    'E', ['Es', 'El', 'Eif', 'Ew', 'Ef', 'Eas', 'Ear'], [r22,r23,r24,r25,r26,r27,r28])

# string expression productions
hulk_grammar.add_attributed_production('Es', ['Es @ Ts', 'Es @@ Ts', 'Ts'], [r29,r30,r31])
hulk_grammar.add_attributed_production('Ts', ['Eb'], [r32])

# boolean expression productions
hulk_grammar.add_attributed_production('Eb', ['Eb | Fb', 'Tb'], [r33,r34])
hulk_grammar.add_attributed_production('Tb', ['Tb & Fb', 'Fb'], [r35,r36])
hulk_grammar.add_attributed_production('Fb', ['! Cb', 'Cb'], [r37,r38])
hulk_grammar.add_attributed_production(
    'Cb', ['Gb == Gb', 'Gb < Gb', 'Gb > Gb', 'Gb >= Gb', 'Gb <= Gb', 'Gb'], [r39,r40,r41,r42,r43,r44])
hulk_grammar.add_attributed_production('Gb', ['Ea'], [r45])

# arithmetic expression productions
hulk_grammar.add_attributed_production('Ea', ['Ea + Ta', 'Ea - Ta', 'Ta'], [r46,r47,r48])
hulk_grammar.add_attributed_production('Ta', ['Ta * Fa', 'Ta / Fa', 'Fa'], [r49,r50,r51])
hulk_grammar.add_attributed_production('Fa', ['Ga ^ Fa', 'Ga'], [r52,r53])
hulk_grammar.add_attributed_production('Ga', ['+ Oa', '- Oa', 'Oa'], [r54,r55,r56])
hulk_grammar.add_attributed_production('Oa', ['W'], [r57])
hulk_grammar.add_attributed_production(
    'W', ['Ids', 'num', 'bool', 'str', '( E )', 'Et'], [r58,r59,r60,r61,r62,r63])

# type productions
hulk_grammar.add_attributed_production('T', [': id', ''], [r64,r65])

# let productions
hulk_grammar.add_attributed_production('El', ['let As in E'], [r66])

hulk_grammar.add_attributed_production('Bl', ['let As in IB'], [r67])

hulk_grammar.add_attributed_production('Il', ['let As ;'], [r68])

hulk_grammar.add_attributed_production('Eas', ['Ids := E'], [r69])

# declarations productions
hulk_grammar.add_attributed_production('As', ['As , Sl', 'Sl'], [r70,rs1])
hulk_grammar.add_attributed_production('Sl', ['id T = E'], [r71])

# if productions
hulk_grammar.add_attributed_production('Hif', ['if ( Eb )'], [r72])
hulk_grammar.add_attributed_production('Helif', ['elif ( Eb )'], [r73])

hulk_grammar.add_attributed_production(
    'Eif', ['Hif E Eelifs else E'], [r74])
hulk_grammar.add_attributed_production('Eelifs', ['Eelifs Eelif', ''], [r75,r76])
hulk_grammar.add_attributed_production('Eelif', ['Helif E'], [r77])

hulk_grammar.add_attributed_production(
    'Bif', ['Hif IBif Belifs Belse'], [r78])
hulk_grammar.add_attributed_production('Belifs', ['Belifs Belif', ''], [r79,r80])
hulk_grammar.add_attributed_production('Belif', ['Helif IBif'], [r81])
hulk_grammar.add_attributed_production('Belse', ['else IBif', ''], [r82,r83])

# while productions
hulk_grammar.add_attributed_production('Hw', ['while ( Eb )'], [r84])

hulk_grammar.add_attributed_production('Ew', ['Hw E'], [r85])

hulk_grammar.add_attributed_production('Bw', ['Hw IB'], [r85])

# # for productions
# hulk_grammar.add_attributed_production(
#     'Hf', ['for ( id in E )'], [])

# hulk_grammar.add_attributed_production('Ef', ['Hf E'], [])
hulk_grammar.add_attributed_production('Ef', ['for ( id in E ) E'], [r86])

# hulk_grammar.add_attributed_production('Bf', ['Hf IB'], [])
hulk_grammar.add_attributed_production('Bf', ['for ( id in E ) IB'], [r86])

# function call productions
hulk_grammar.add_attributed_production('Ec', ['id ( C1 )'], [r87])
hulk_grammar.add_attributed_production('C1', ['C2', ''], [r88, r89])
hulk_grammar.add_attributed_production('C2', ['E , C2', 'E'], [r90, r91])

# variable productions
hulk_grammar.add_attributed_production('Ids', ['Ids . Q', 'Q'], [])
hulk_grammar.add_attributed_production('Q', ['id', 'Ec', 'Ac'], [lambda h,s: s[1], lambda h,s: s[1], lambda h,s: s[1]])

# function productions
# hulk_grammar.add_attributed_production('Fh', ['( D1 )'], [lambda h,s: s[2]])
# hulk_grammar.add_attributed_production('D1', ['', 'D2'], [rs0, r1])
# hulk_grammar.add_attributed_production('D2', ['D3 , D2', 'D3'], [])
# hulk_grammar.add_attributed_production('D3', ['id T'], [])

# hulk_grammar.add_attributed_production('F', ['function id Fh T FB'], [lambda h,s: FunctionDeclarationNode(s[2], s[3], s[5], s[4])])
# hulk_grammar.add_attributed_production('FB', ['IB', '=> E ;'], [lambda h,s: s[1], lambda h,s: s[2]])

hulk_grammar.add_attributed_production('Fh', ['( D1 )'], [])
hulk_grammar.add_attributed_production('D1', ['', 'D2'], [rs0, r1])
hulk_grammar.add_attributed_production('D2', ['D3 , D2', 'D3'], [])
hulk_grammar.add_attributed_production('D3', ['id T'], [])

hulk_grammar.add_attributed_production('F', ['function id Fh T FB'], [])
hulk_grammar.add_attributed_production('FB', ['IB', '=> E ;'], [])

hulk_grammar.add_attributed_production('Hc', ['type Fh', 'type id'], [])
hulk_grammar.add_attributed_production(
    'Hih', ['inherits Ec', 'inherits id', ''], [])

hulk_grammar.add_attributed_production('C', ['Hc Hih { CB }'], [])
hulk_grammar.add_attributed_production('CB', ['CB IC', ''], [])
hulk_grammar.add_attributed_production('IC', ['id T = E ;', 'Fh T FB'], [])

hulk_grammar.add_attributed_production(
    'Et', ['Ids is id', 'Ids as id', 'new Ec'], [])

hulk_grammar.add_attributed_production('Ear', ['[ X1 ]'], [])
hulk_grammar.add_attributed_production('X1', ['E || id in E', 'X2', ''], [])
hulk_grammar.add_attributed_production('X2', ['X2 , E', 'E'], [])

hulk_grammar.add_attributed_production('Ac', ['id Y1'], [])
hulk_grammar.add_attributed_production('Y1', ['Y1 [ E ]', '[ E ]'], [])

hulk_grammar.add_attributed_production('Pr', ['protocol id Pe { PB }'], [])
hulk_grammar.add_attributed_production('Pe', ['extends id', ''], [])
hulk_grammar.add_attributed_production('PB', ['PB Fh T ;', 'Fh T ;'], [])
