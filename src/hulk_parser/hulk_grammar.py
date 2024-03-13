from compiler_tools.grammar import GrammarToken,EOF
from compiler_tools.attributed_grammar import AttributedGrammar,AttributedRule
# from hulk_parser.hulk_ast import *

hulk_grammar = AttributedGrammar()

hulk_grammar.add_main('P')
hulk_grammar.add_attributed_production('P', ['Is'], [])
hulk_grammar.add_attributed_production('B',['{ Is }'],[])
hulk_grammar.add_attributed_production('Is', ['I Is', 'I'], [])
hulk_grammar.add_attributed_production('I', ['I1'], [])

hulk_grammar.add_attributed_production('Is1', ['I1 Is1','I1'], [])
hulk_grammar.add_attributed_production('I1',['E ;','E'],[])
hulk_grammar.add_attributed_production('E',['El'],[])

# hulk_grammar.add_attributed_production('Ea',['Ea + Ta','Ea - Ta','Ta'],[])
# hulk_grammar.add_attributed_production('Ta',['Ta * Fa', 'Ta / Fa','Fa'],[])
# hulk_grammar.add_attributed_production('Fa',['Ga ^ Fa','Ga ** Fa', 'Ga'],[])
# hulk_grammar.add_attributed_production('Ga',['num','Eb'],[])

# hulk_grammar.add_attributed_production('Eb',['Eb | Tb','Tb'],[])
# hulk_grammar.add_attributed_production('Tb',['Tb & Fb','Fb'],[])
# hulk_grammar.add_attributed_production('Fb',['! Gb','Gb'],[])
# hulk_grammar.add_attributed_production('Gb',['True','False','Es'],[])

# hulk_grammar.add_attributed_production('Es',['Es @ Ts','Es @@ Ts','Ts'],[])
# hulk_grammar.add_attributed_production('Ts',['string','W'],[])

# hulk_grammar.add_attributed_production('W',['id','( E )','El'],[])
# hulk_grammar.add_attributed_production('T',[': id',''],[])

hulk_grammar.add_attributed_production('El',['let Sl Bl'],[])
# hulk_grammar.add_attributed_production('Al',['Sl , Al','Sl'],[])
hulk_grammar.add_attributed_production('Sl',['id T = E'],[])
hulk_grammar.add_attributed_production('Bl',['in B',''],[])

# hulk_grammar.add_attributed_production('Eif',['if ( E ) X else X'],[])
# hulk_grammar.add_attributed_production('X',['E'],[])
# hulk_grammar.add_attributed_production('B1',['B1 elif X', ''],[])
# hulk_grammar.add_attributed_production('B2',['else X', ''],[])

hulk_grammar.calculate_follow()





