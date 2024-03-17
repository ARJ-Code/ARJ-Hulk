from compiler_tools.attributed_grammar import AttributedGrammar, AttributedRule

hulk_grammar = AttributedGrammar()

hulk_grammar.add_main('P')

hulk_grammar.add_attributed_production('P', ['P1'], [])
hulk_grammar.add_attributed_production(
    'P1', ['I2s EB ; I2s', 'I2s EB I2s'], [])
hulk_grammar.add_attributed_production('I1s', ['I1s E ;', 'E ;'], [])
hulk_grammar.add_attributed_production(
    'I2s', ['I2s I', ''], [])
hulk_grammar.add_attributed_production('I', ['C', 'F', 'Pr'], [])

hulk_grammar.add_attributed_production('B', ['{ I1s }'], [])

hulk_grammar.add_attributed_production(
    'E', ['Es', 'El', 'Eif', 'Ew', 'Ef', 'Eas', 'Ear'], [])

hulk_grammar.add_attributed_production('Es', ['Es @ Ts', 'Es @@ Ts', 'Ts'], [])
hulk_grammar.add_attributed_production('Ts', ['Eb'], [])

hulk_grammar.add_attributed_production('Eb', ['Eb | Fb', 'Tb'], [])
hulk_grammar.add_attributed_production('Tb', ['Tb & Fb', 'Fb'], [])
hulk_grammar.add_attributed_production('Fb', ['! Cb', 'Cb'], [])
hulk_grammar.add_attributed_production(
    'Cb', ['Gb == Gb', 'Gb < Gb', 'Gb > Gb', 'Gb >= Gb', 'Gb <= Gb', 'Gb'], [])
hulk_grammar.add_attributed_production('Gb', ['Ea'], [])

hulk_grammar.add_attributed_production('Ea', ['Ea + Ta', 'Ea - Ta', 'Ta'], [])
hulk_grammar.add_attributed_production('Ta', ['Ta * Fa', 'Ta / Fa', 'Fa'], [])
hulk_grammar.add_attributed_production('Fa', ['Ga ^ Fa', 'Ga'], [])
hulk_grammar.add_attributed_production('Ga', ['+ Oa', '- Oa', 'Oa'], [])
hulk_grammar.add_attributed_production('Oa', ['W'], [])

hulk_grammar.add_attributed_production(
    'W', ['Ids', 'num', 'bool', 'str', '( E )', 'Et'], [])
hulk_grammar.add_attributed_production('T', [': id', ''], [])

hulk_grammar.add_attributed_production('EB', ['E', 'B'], [])

hulk_grammar.add_attributed_production('El', ['let As in EB'], [])
hulk_grammar.add_attributed_production('As', ['As , Sl', 'Sl'], [])
hulk_grammar.add_attributed_production('Sl', ['id T = E'], [])

hulk_grammar.add_attributed_production('Eas', ['Ids := E'], [])

hulk_grammar.add_attributed_production(
    'Eif', ['if ( Eb ) EB Eelifs else EB'], [])
hulk_grammar.add_attributed_production('Eelifs', ['Eelif Eelifs', ''], [])
hulk_grammar.add_attributed_production('Eelif', ['elif ( Eb ) EB'], [])

hulk_grammar.add_attributed_production('Ew', ['while ( Eb ) EB'], [])

hulk_grammar.add_attributed_production('Ef', ['for ( id in E ) EB'], [])

hulk_grammar.add_attributed_production('Ec', ['id ( C1 )'], [])
hulk_grammar.add_attributed_production('C1', ['C2', ''], [])
hulk_grammar.add_attributed_production('C2', ['E , C2', 'E'], [])

hulk_grammar.add_attributed_production('Ids', ['Ids . Q', 'Q'], [])
hulk_grammar.add_attributed_production('Q', ['id', 'Ec', 'Ac'], [])

hulk_grammar.add_attributed_production('D1', ['', 'D2'], [])
hulk_grammar.add_attributed_production('D2', ['D3 , D2', 'D3'], [])
hulk_grammar.add_attributed_production('D3', ['id T'], [])

hulk_grammar.add_attributed_production('F', ['function id ( D1 ) T FB'], [])
hulk_grammar.add_attributed_production('FB', ['B', '=> E ;'], [])

hulk_grammar.add_attributed_production('Hc', ['type id ( D2 )', 'type id'], [])
hulk_grammar.add_attributed_production(
    'Hih', ['inherits id ( C2 )', 'inherits id', ''], [])

hulk_grammar.add_attributed_production('C', ['Hc Hih { CB }'], [])
hulk_grammar.add_attributed_production('CB', ['CB IC', ''], [])
hulk_grammar.add_attributed_production('IC', ['id T = E ;', 'id ( D1 ) T FB'], [])

hulk_grammar.add_attributed_production(
    'Et', ['Ids is id', 'Ids as id', 'new Ec'], [])

hulk_grammar.add_attributed_production('Ear', ['[ X1 ]'], [])
hulk_grammar.add_attributed_production('X1', ['E || id in E', 'X2', ''], [])
hulk_grammar.add_attributed_production('X2', ['X2 , E', 'E'], [])

hulk_grammar.add_attributed_production('Ac', ['id Y1'], [])
hulk_grammar.add_attributed_production('Y1', ['Y1 [ E ]', '[ E ]'], [])

hulk_grammar.add_attributed_production(
    'Pr', ['protocol id { PB }', 'protocol id extends id { PB }'], [])
hulk_grammar.add_attributed_production('PB', ['PB id ( D1 ) T ;', 'id ( D1 ) T ;'], [])
