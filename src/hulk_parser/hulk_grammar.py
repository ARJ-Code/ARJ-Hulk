from compiler_tools.attributed_grammar import AttributedGrammar, AttributedRule

hulk_grammar = AttributedGrammar()

hulk_grammar.add_main('P')

hulk_grammar.add_attributed_production('P', ['Is'], [])
hulk_grammar.add_attributed_production('Is', ['Is I', 'I'], [])
hulk_grammar.add_attributed_production('I', ['I1', 'I2'], [])

hulk_grammar.add_attributed_production('I1', ['E ;', 'IB', ';'], [])
hulk_grammar.add_attributed_production('I1s', ['I1s I1', 'I1'], [])
hulk_grammar.add_attributed_production(
    'IB', ['B', 'Bl', 'Bw', 'Bf', 'Bif'], [])
hulk_grammar.add_attributed_production(
    'IBif', ['B', 'E ;'], [])
hulk_grammar.add_attributed_production('B', ['{ I1s }'], [])

hulk_grammar.add_attributed_production('I2', ['C', 'F'], [])

hulk_grammar.add_attributed_production(
    'E', ['Es', 'El', 'Eif', 'Ew', 'Ef'], [])

hulk_grammar.add_attributed_production('Es', ['Es @ Ts', 'Es @@ Ts', 'Ts'], [])
hulk_grammar.add_attributed_production('Ts', ['string', 'Eb'], [])

hulk_grammar.add_attributed_production('Eb', ['Eb | Fb', 'Tb'], [])
hulk_grammar.add_attributed_production('Tb', ['Tb & Fb', 'Fb'], [])
hulk_grammar.add_attributed_production('Fb', ['! Cb', 'Cb'], [])
hulk_grammar.add_attributed_production(
    'Cb', ['Gb == Gb', 'Gb < Gb', 'Gb > Gb', 'Gb >= Gb', 'Gb <= Gb'], [])
hulk_grammar.add_attributed_production('Gb', ['true', 'false', 'Ea'], [])

hulk_grammar.add_attributed_production('Ea', ['Ea + Ta', 'Ea - Ta', 'Ta'], [])
hulk_grammar.add_attributed_production('Ta', ['Ta * Fa', 'Ta / Fa', 'Fa'], [])
hulk_grammar.add_attributed_production('Fa', ['Ga ^ Fa', 'Ga'], [])
hulk_grammar.add_attributed_production('Ga', ['+ Oa', '- Oa', 'Oa'], [])
hulk_grammar.add_attributed_production('Oa', ['num', 'W'], [])

hulk_grammar.add_attributed_production('W', ['Ids', '( E )', 'Et'], [])
hulk_grammar.add_attributed_production('T', [': id', ''], [])

hulk_grammar.add_attributed_production('El', ['let As BEL'], [])
hulk_grammar.add_attributed_production('As', ['As , Sl', 'Sl'], [])
hulk_grammar.add_attributed_production('Sl', ['id T = Es'], [])
hulk_grammar.add_attributed_production('BEl', ['in E', ''], [])

hulk_grammar.add_attributed_production('Bl', ['let As in IB'], [])

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
    'Hf', ['for ( id in range ( E , E ) )'], [])

hulk_grammar.add_attributed_production('Ef', ['Hf E'], [])

hulk_grammar.add_attributed_production('Bf', ['Hf IB'], [])

hulk_grammar.add_attributed_production('Ec', ['id ( C1 )'], [])
hulk_grammar.add_attributed_production('C1', ['C2', ''], [])
hulk_grammar.add_attributed_production('C2', ['E , C2'], [])

hulk_grammar.add_attributed_production('Ids', ['Ids . Q', 'Q'], [])
hulk_grammar.add_attributed_production('Q', ['id', 'Ec'], [])

hulk_grammar.add_attributed_production('Fh', ['id ( D1 )'], [])
hulk_grammar.add_attributed_production('D1', ['', 'D2'], [])
hulk_grammar.add_attributed_production('D2', ['D3 , D2', 'D3'], [])
hulk_grammar.add_attributed_production('D3', ['id T'], [])

hulk_grammar.add_attributed_production('F', ['function Fh FB'], [])
hulk_grammar.add_attributed_production('FB', ['IB', '=> E ;'], [])

hulk_grammar.add_attributed_production('Hc', ['type Fh', 'type id'], [])
hulk_grammar.add_attributed_production(
    'Hih', ['inherit Ec', 'inherit id', ''], [])

hulk_grammar.add_attributed_production('C', ['Hc Hih { CB }'], [])
hulk_grammar.add_attributed_production('CB', ['CB IC', ''], [])
hulk_grammar.add_attributed_production('IC', ['Cp', 'F'], [])
hulk_grammar.add_attributed_production('Cp', ['id T = E ;'], [])

hulk_grammar.add_attributed_production(
    'Et', ['Ids is id', 'Ids as id', 'new Ec'],[])
