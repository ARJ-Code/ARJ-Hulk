from compiler_tools.attributed_grammar import AttributedGrammar, AttributedRule
from compiler_tools.lexer import LexerToken
from hulk.hulk_ast import *

hulk_grammar = AttributedGrammar()

hulk_grammar.add_main('P')

empty_list = AttributedRule[ASTNode, LexerToken](lambda _, s: [])
first_list = AttributedRule[ASTNode, LexerToken](lambda _, s: [s[1]])

first = AttributedRule[ASTNode, LexerToken](lambda _, s: s[1])
second = AttributedRule[ASTNode, LexerToken](lambda _, s: s[2])

# program productions
hulk_grammar.add_attributed_production('P', ['P1'], [first])

program_node1 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ProgramNode(s[1], s[2], s[4]))
program_node2 = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ProgramNode(s[1], s[2], s[3]))
hulk_grammar.add_attributed_production(
    'P1', ['I2s EB ; I2s', 'I2s EB I2s'], [program_node1, program_node2])


push_second_to_first = AttributedRule[ASTNode, LexerToken](lambda h, s: s[1] + [s[2]])
push_first_to_3th = AttributedRule[ASTNode, LexerToken](
    lambda h, s: [s[1]] + s[3])
push_3th_to_first = AttributedRule[ASTNode, LexerToken](lambda h, s: s[1] + [s[3]])


# instructions productions
hulk_grammar.add_attributed_production('I2s', ['I2s I', ''], [push_second_to_first, empty_list])


hulk_grammar.add_attributed_production('I', ['C', 'F', 'Pr'], [first, first, first])


# expression productions
hulk_grammar.add_attributed_production('EB', ['E', 'B'], [first, first])

exp_block = AttributedRule[ASTNode, LexerToken](lambda _, s: ExpressionBlockNode(s[2]))
hulk_grammar.add_attributed_production('B', ['{ I1s }'], [exp_block])

hulk_grammar.add_attributed_production('I1s', ['I1s E ;', 'E ;'], [push_second_to_first, first_list])

hulk_grammar.add_attributed_production(
    'E', ['Es', 'El', 'Eif', 'Ew', 'Ef', 'Eas', 'Ear'], [first, first, first, first, first, first, first])


# string expression productions
concat_str = AttributedRule[ASTNode, LexerToken](
    lambda h, s: StringBinaryNode(s[1], s[3], StringOperator.CONCAT))
concat_str_space = AttributedRule[ASTNode, LexerToken](
    lambda h, s: StringBinaryNode(s[1], s[3], StringOperator.SPACED_CONCAT))
hulk_grammar.add_attributed_production(
    'Es', ['Es @ Ts', 'Es @@ Ts', 'Ts'], [concat_str, concat_str_space, first])

hulk_grammar.add_attributed_production('Ts', ['Eb'], [first])


# boolean expression productions
or_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.OR))
hulk_grammar.add_attributed_production('Eb', ['Eb | Fb', 'Tb'], [or_op, first])

and_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.AND))
hulk_grammar.add_attributed_production('Tb', ['Tb & Fb', 'Fb'], [and_op, first])

not_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanUnaryNode(s[2], BooleanOperator.NOT))
hulk_grammar.add_attributed_production('Fb', ['! Cb', 'Cb'], [not_op, first])

eq_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.EQ))
neq_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.NEQ))
lt_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.LT))
gt_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.GT))
gte_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.GTE))
lte_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: BooleanBinaryNode(s[1], s[3], BooleanOperator.LTE))
hulk_grammar.add_attributed_production(
    'Cb', ['Gb == Gb', 'Gb != Gb', 'Gb < Gb', 'Gb > Gb', 'Gb >= Gb', 'Gb <= Gb', 'Gb'], [eq_op, neq_op, lt_op, gt_op, gte_op, lte_op, first])

hulk_grammar.add_attributed_production('Gb', ['Ea'], [first])


# arithmetic expression productions
add_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticBinaryNode(s[1], s[3], ArithmeticOperator.ADD))
sub_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticBinaryNode(s[1], s[3], ArithmeticOperator.SUB))
hulk_grammar.add_attributed_production(
    'Ea', ['Ea + Ta', 'Ea - Ta', 'Ta'], [add_op, sub_op, first])

mul_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticBinaryNode(s[1], s[3], ArithmeticOperator.MUL))
div_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticBinaryNode(s[1], s[3], ArithmeticOperator.DIV))
hulk_grammar.add_attributed_production(
    'Ta', ['Ta * Fa', 'Ta / Fa', 'Fa'], [mul_op, div_op, first])

pow_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticBinaryNode(s[1], s[3], ArithmeticOperator.POW))
hulk_grammar.add_attributed_production('Fa', ['Ga ^ Fa', 'Ga'], [pow_op, first])

plus_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticUnaryNode(s[2], ArithmeticOperator.ADD))
minus_op = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArithmeticUnaryNode(s[2], ArithmeticOperator.SUB))
hulk_grammar.add_attributed_production(
    'Ga', ['+ Oa', '- Oa', 'Oa'], [plus_op, minus_op, first])

hulk_grammar.add_attributed_production('Oa', ['W'], [first])

num_c = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ConstantNode(s[1], ConstantTypes.NUMBER))
bool_c = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ConstantNode(s[1], ConstantTypes.BOOLEAN))
str_c = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ConstantNode(s[1], ConstantTypes.STRING))
atomic = AttributedRule[ASTNode, LexerToken](
    lambda h, s: AtomicNode(s[1]))
inst_prop = AttributedRule[ASTNode, LexerToken](
    lambda h, s: InstancePropertyNode(s[1], s[3]))
inst_func = AttributedRule[ASTNode, LexerToken](
    lambda h, s: InstanceFunctionNode(s[1], s[3]))
inst_func_atomic = AttributedRule[ASTNode, LexerToken](
    lambda h, s: InstanceFunctionNode(AtomicNode(s[1]), s[3]))
inst_func_prop = AttributedRule[ASTNode, LexerToken](
    lambda h, s: InstanceFunctionNode(InstancePropertyNode(s[1], s[3]), s[5]))

hulk_grammar.add_attributed_production(
    'Epc', ['Epc . Ec', 'Ec . Ec', 'id . Ec', 'id . id . Ec'], [inst_func, inst_func, inst_func_atomic,inst_func_prop ])

hulk_grammar.add_attributed_production(
    'W', ['id', 'id . id', 'num', 'bool', 'str', '( E )', 'Et', 'Ec', 'Epc', 'Ac'], [atomic, inst_prop, num_c, bool_c, str_c, second, first, first, first, first])


# type productions
eof_type = AttributedRule[ASTNode, LexerToken](lambda h, s: EOFTypeNode())
hulk_grammar.add_attributed_production('T', [': Type', ''], [second, eof_type])


nt = AttributedRule[ASTNode, LexerToken](lambda h, s: TypeNode(s[1]))
vt = AttributedRule[AsNode, LexerToken](
    lambda h, s: VectorTypeNode(s[2], None))
vtd = AttributedRule[AsNode, LexerToken](
    lambda h, s: VectorTypeNode(s[2], s[4]))
hulk_grammar.add_attributed_production(
    'Type', ['id', '[ id ]', '[ id , num ]'], [nt, vt, vtd])


# declarations productions
declaration = AttributedRule[ASTNode, LexerToken](
    lambda h, s: DeclarationNode(s[1], s[2], s[4]))
hulk_grammar.add_attributed_production('Sl', ['id T = E'], [declaration])

assign = AttributedRule[ASTNode, LexerToken](
    lambda h, s: AssignmentNode(s[1], s[3]))

assign_arr = AttributedRule[ASTNode, LexerToken](
    lambda h, s: AssignmentArrayNode(s[1], s[3]))

assign_prop = AttributedRule[ASTNode, LexerToken](
    lambda h, s: AssignmentPropertyNode(s[1], s[3], s[5]))

hulk_grammar.add_attributed_production(
    'Eas', ['id := E', 'Ac := E', 'id . id := E'], [assign, assign_arr, assign_prop])


# let productions
let_n = AttributedRule[ASTNode, LexerToken](lambda h, s: LetNode(s[2], s[4]))
hulk_grammar.add_attributed_production('El', ['let As in EB'], [let_n])

hulk_grammar.add_attributed_production('As', ['Sl , As', 'Sl'], [push_first_to_3th, first_list])


# if productions
if_n = AttributedRule[ASTNode, LexerToken](
    lambda h, s: IfNode(s[3], s[5], s[6], s[8]))
hulk_grammar.add_attributed_production(
    'Eif', ['if ( Eb ) EB Eelifs else EB'], [if_n])

hulk_grammar.add_attributed_production(
    'Eelifs', ['Eelifs Eelif', ''], [push_second_to_first, empty_list])

elif_n = AttributedRule[ASTNode, LexerToken](lambda h, s: ElifNode(s[3], s[5]))
hulk_grammar.add_attributed_production('Eelif', ['elif ( Eb ) EB'], [elif_n])


# while productions
while_n = AttributedRule[ASTNode, LexerToken](lambda h, s: WhileNode(s[3], s[5]))
hulk_grammar.add_attributed_production('Ew', ['while ( Eb ) EB'], [while_n])


# for productions
for_n = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ForNode(s[3], s[5], s[7]))
hulk_grammar.add_attributed_production('Ef', ['for ( id in E ) EB'], [for_n])


# function call productions
exp_c = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ExpressionCallNode(s[1], s[3]))
hulk_grammar.add_attributed_production('Ec', ['id ( C1 )'], [exp_c])

hulk_grammar.add_attributed_production('C1', ['C2', ''], [first, empty_list])

hulk_grammar.add_attributed_production('C2', ['E , C2', 'E'], [push_first_to_3th, first_list])

# function productions
function_n = AttributedRule[ASTNode, LexerToken](
    lambda h, s: FunctionDeclarationNode(s[2], s[4], s[6], s[7]))
hulk_grammar.add_attributed_production(
    'F', ['function id ( D1 ) T FB'], [function_n])

hulk_grammar.add_attributed_production('FB', ['B', '=> E ;'], [first, second])

hulk_grammar.add_attributed_production('D1', ['D2', ''], [first, empty_list])

hulk_grammar.add_attributed_production('D2', ['D3 , D2', 'D3'], [push_first_to_3th, first_list])

param_n = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ParameterNode(s[1], s[2]))
hulk_grammar.add_attributed_production('D3', ['id T'], [param_n])


# class productions
class_tn = AttributedRule[ASTNode, LexerToken](lambda h, s: ClassTypeNode(s[2]))
class_tpn = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ClassTypeParameterNode(s[2], s[4]))
hulk_grammar.add_attributed_production(
    'Hc', ['type id', 'type id ( D1 )'], [class_tn, class_tpn])

inherits_n = AttributedRule[ASTNode, LexerToken](lambda h, s: InheritanceNode(s[2]))
inherits_pn = AttributedRule[ASTNode, LexerToken](
    lambda h, s: InheritanceParameterNode(s[2], s[4]))
eof_inheritance = AttributedRule[ASTNode, LexerToken](
    lambda h, s: EOFInheritsNode())
hulk_grammar.add_attributed_production(
    'Hih', ['inherits id', 'inherits id ( C2 )', ''], [inherits_n, inherits_pn, eof_inheritance])

class_n = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ClassDeclarationNode(s[1], s[2], s[4]))
hulk_grammar.add_attributed_production('C', ['Hc Hih { CB }'], [class_n])

hulk_grammar.add_attributed_production('CB', ['CB IC', ''], [push_second_to_first, empty_list])

class_pn = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ClassPropertyNode(s[1], s[2], s[4]))
class_fn = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ClassFunctionNode(s[1], s[3], s[5], s[6]))
hulk_grammar.add_attributed_production(
    'IC', ['id T = E ;', 'id ( D1 ) T FB'], [class_pn, class_fn])


# type inference productions
r47 = AttributedRule[ASTNode, LexerToken](lambda h, s: IsNode(s[1], s[3]))
r48 = AttributedRule[ASTNode, LexerToken](lambda h, s: AsNode(s[1], s[3]))
r49 = AttributedRule[ASTNode, LexerToken](lambda h, s: NewNode(s[2]))
hulk_grammar.add_attributed_production(
    'Et', ['W is id', 'W as id', 'new Ec'], [r47, r48, r49])


# vector productions
hulk_grammar.add_attributed_production('Ear', ['[ X1 ]'], [second])

array_imp = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ImplicitArrayDeclarationNode(s[1], s[3], s[5]))
array_exp = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ExplicitArrayDeclarationNode(s[1]))
array_exp_empty = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ExplicitArrayDeclarationNode([]))
hulk_grammar.add_attributed_production(
    'X1', ['E || id in E', 'X2', ''], [array_imp, array_exp, array_exp_empty])

hulk_grammar.add_attributed_production('X2', ['X2 , E', 'E'], [push_3th_to_first, first_list])


# vector indexation productions
array_call_atomic = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArrayCallNode(AtomicNode(s[1]), s[3]))

array_call = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ArrayCallNode(s[1], s[3]))
hulk_grammar.add_attributed_production(
    'Ac', ['id [ E ]', 'Ec [ E ]', 'Ac [ E ]', 'Epc [ E ]'], [array_call_atomic, array_call, array_call, array_call])


# protocol productions
protocol_tn = AttributedRule[ASTNode, LexerToken](lambda h, s: ProtocolTypeNode(s[2]))
hulk_grammar.add_attributed_production('PT', ['protocol id'], [protocol_tn])

extension_n = AttributedRule[ASTNode, LexerToken](lambda h, s: ExtensionNode(s[2]))
eof_extension = AttributedRule[ASTNode, LexerToken](
    lambda h, s: EOFExtensionNode())
hulk_grammar.add_attributed_production(
    'Prex', ['extends id', ''], [extension_n, eof_extension])

protocol_n = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ProtocolDeclarationNode(s[1], s[2], s[4]))
hulk_grammar.add_attributed_production('Pr', ['PT Prex { PB }'], [protocol_n])

hulk_grammar.add_attributed_production('PB', ['PB PF', 'PF'], [push_second_to_first, first_list])

protocol_fn = AttributedRule[ASTNode, LexerToken](
    lambda h, s: ProtocolFunctionNode(s[1], s[3], s[5]))
hulk_grammar.add_attributed_production('PF', ['id ( D1 ) T ;'], [protocol_fn])
