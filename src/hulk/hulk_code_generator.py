from .hulk_ast import *
import compiler_tools.visitor as visitor
from typing import Dict, List
from .hulk_defined import is_defined_method

B1 = '{'
B2 = '}'


def define_v(v: str):
    return f'Type *{v}'


def new_number(v: str):
    return f'system_createNumber({v})'


def new_boolean(v: str):
    return f'system_createBoolean({v})'


def new_string(v: str):
    return f'system_createString({v})'


class GeneratorContext:
    def __init__(self):
        self.dict_v: Dict[str, str] = {}
        self.curr_v: int = 0
        self.indentation: int = 0
        self.code: List[str] = []
        self.stack_v: List[str] = []

    def new_line(self, line: str):
        if line == '}':
            self.indentation -= 1

        tabs = '\t'*self.indentation

        self.code.append(tabs+line)
        if line == '{':
            self.indentation += 1

    def new_v(self) -> str:
        v = 'v'+str(self.curr_v)
        self.curr_v += 1
        return v

    def get_v(self, v: str) -> str:
        if not v in self.dict_v:
            self.dict_v[v] = self.new_v()

        return self.dict_v[v]

    def get_code(self):
        return '\n'.join(l for l in self.code)

    def push_v(self, v: str):
        self.stack_v.append(v)

    def pop_v(self) -> str:
        v = self.stack_v[-1]
        self.stack_v.pop()

        return v

    def top_v(self) -> str:
        return self.stack_v[-1]


class HulkCodeGenerator(object):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> str:
        context = GeneratorContext()

        context.new_line('int main()')
        context.new_line('{')
        context.new_line('srand48(time(NULL));')

        context.push_v(context.new_v())
        self.visit(node.expression, context)

        context.new_line('}')

        return context.get_code()

    @visitor.when(ConstantNode)
    def visit(self, node: ConstantNode, context: GeneratorContext):
        if node.type == ConstantTypes.BOOLEAN:
            v = 1 if node.value.value == 'true' else 0
            context.new_line(
                f'{define_v(context.pop_v())} = system_createBoolean({v});')
        if node.type == ConstantTypes.STRING:
            context.new_line(
                f'{define_v(context.pop_v())} = system_createString("{node.value.value[1:-1]}");')
        if node.type == ConstantTypes.NUMBER:
            context.new_line(
                f'{define_v(context.pop_v())} = system_createNumber({node.value.value});')

    @visitor.when(ExplicitArrayDeclarationNode)
    def visit(self, node: ExplicitArrayDeclarationNode, context: GeneratorContext):
        vec = context.pop_v()
        context.new_line(f'{define_v(vec)} = system_createList();')

        for e in node.values:
            v = context.new_v()
            context.push_v(v)

            self.visit(e, context)
            context.new_line(f'system_addList({vec}, {v});')

    @visitor.when(ImplicitArrayDeclarationNode)
    def visit(self, node: ImplicitArrayDeclarationNode, context: GeneratorContext):
        vec = context.pop_v()
        context.new_line(f'{define_v(vec)} = system_createList();')

        vi = context.new_v()
        context.push_v(vi)
        self.visit(node.iterable, context)

        v = context.get_v(node.variable.value)

        context.new_line(f'system_reset({vi});')
        context.new_line(f'while(system_typeToBoolean(system_next({vi})))')
        context.new_line('{')

        context.new_line(f'{define_v(v)} = system_current({vi});')

        exp = context.new_v()
        context.push_v(exp)

        self.visit(node.expression, context)
        context.new_line(f'system_addList({vec}, {exp});')

        context.new_line('}')

    @visitor.when(StringBinaryNode)
    def visit(self, node: StringBinaryNode, context: GeneratorContext):
        lv = context.new_v()
        context.push_v(lv)
        self.visit(node.left, context)

        rv = context.new_v()
        context.push_v(rv)
        self.visit(node.right, context)

        if node.operator == StringOperator.CONCAT:
            context.new_line(
                f'{define_v(context.pop_v())} = system_concatString({lv}, {rv});')
        if node.operator == StringOperator.SPACED_CONCAT:
            context.new_line(
                f'{define_v(context.pop_v())} = system_concatWithSpaceString({lv}, {rv});')

    @visitor.when(ArithmeticBinaryNode)
    def visit(self, node: ArithmeticBinaryNode, context: GeneratorContext):
        lv = context.new_v()
        context.push_v(lv)
        self.visit(node.left, context)

        rv = context.new_v()
        context.push_v(rv)
        self.visit(node.right, context)

        if node.operator == ArithmeticOperator.ADD:
            context.new_line(
                f'{define_v(context.pop_v())} = system_addNumber({lv}, {rv});')
        if node.operator == ArithmeticOperator.SUB:
            context.new_line(
                f'{define_v(context.pop_v())} = system_subNumber({lv}, {rv});')
        if node.operator == ArithmeticOperator.MUL:
            context.new_line(
                f'{define_v(context.pop_v())} = system_mulNumber({lv}, {rv});')
        if node.operator == ArithmeticOperator.DIV:
            context.new_line(
                f'{define_v(context.pop_v())} = system_divNumber({lv}, {rv});')
        if node.operator == ArithmeticOperator.POW:
            context.new_line(
                f'{define_v(context.pop_v())} = system_powNumber({lv}, {rv});')

    @visitor.when(ArithmeticUnaryNode)
    def visit(self, node: ArithmeticUnaryNode, context: GeneratorContext):
        v = context.new_v()
        context.push_v(v)
        self.visit(node.child, context)

        if node.operator == ArithmeticOperator.ADD:
            context.new_line(
                f'{define_v(context.pop_v())} = system_addNumber(system_createNumber(0), {v});')
        if node.operator == ArithmeticOperator.SUB:
            context.new_line(
                f'{define_v(context.pop_v())} = system_subNumber(system_createNumber(0), {v});')

    @visitor.when(BooleanBinaryNode)
    def visit(self, node: BooleanBinaryNode, context: GeneratorContext):
        lv = context.new_v()
        context.push_v(lv)
        self.visit(node.left, context)

        rv = context.new_v()
        context.push_v(rv)
        self.visit(node.right, context)

        if node.operator == BooleanOperator.AND:
            context.new_line(
                f'{define_v(context.pop_v())} = system_andBoolean({lv}, {rv});')
        if node.operator == BooleanOperator.OR:
            context.new_line(
                f'{define_v(context.pop_v())} = system_orBoolean({lv}, {rv});')
        if node.operator == BooleanOperator.EQ:
            context.new_line(
                f'{define_v(context.pop_v())} = system_eq({lv}, {rv});')
        if node.operator == BooleanOperator.GT:
            context.new_line(
                f'{define_v(context.pop_v())} = system_eq(system_comp({lv}, {rv}), system_createNumber(1));')
        if node.operator == BooleanOperator.LT:
            context.new_line(
                f'{define_v(context.pop_v())} = system_eq(system_comp({lv}, {rv}), system_createNumber(-1));')
        if node.operator == BooleanOperator.GTE:
            context.new_line(
                f'{define_v(context.pop_v())} = system_notBoolean(system_eq(system_comp({lv}, {rv}), system_createNumber(-1)));')
        if node.operator == BooleanOperator.LTE:
            context.new_line(
                f'{define_v(context.pop_v())} = system_notBoolean(system_eq(system_comp({lv}, {rv}), system_createNumber(1)));')
        if node.operator == BooleanOperator.NEQ:
            context.new_line(
                f'{define_v(context.pop_v())} = system_notBoolean(system_eq({lv}, {rv}));')

    @visitor.when(BooleanUnaryNode)
    def visit(self, node: BooleanUnaryNode, context: GeneratorContext):
        v = context.new_v()
        context.push_v(v)
        self.visit(node.child, context)

        if node.operator == BooleanOperator.NOT:
            context.new_line(
                f'{define_v(context.pop_v())} = system_notBoolean({v});')

    @visitor.when(ExpressionCallNode)
    def visit(self, node: ExpressionCallNode, context: GeneratorContext):
        v = []

        for p in node.parameters:
            aux = context.new_v()
            context.push_v(aux)
            v.append(aux)

            self.visit(p, context)

        params = ', '.join(v)

        if is_defined_method(node.name.value):
            context.new_line(
                f'{define_v(context.pop_v())} = system_{node.name.value}({params});')

    @visitor.when(AssignmentNode)
    def visit(self, node: AssignmentNode, context: GeneratorContext):
        vn = context.get_v(node.name.value)
        vc = context.new_v()
        context.push_v(vc)

        self.visit(node.value, context)

        context.new_line(f'{vn} = {vc};')
        context.new_line(f'{define_v(context.pop_v())} = {vc};')

    @visitor.when(AtomicNode)
    def visit(self, node: AtomicNode, context: GeneratorContext):
        context.new_line(
            f'{define_v(context.pop_v())} = {context.get_v(node.name.value)};')

    @visitor.when(ExpressionBlock)
    def visit(self, node: ExpressionBlock, context: GeneratorContext):
        for n in node.instructions[:-1]:
            v = context.new_v()
            context.push_v(v)
            self.visit(n, context)

        self.visit(node.instructions[-1], context)

    @visitor.when(LetNode)
    def visit(self, node: LetNode, context: GeneratorContext):
        for a in node.assignments:
            vn = context.get_v(a.name.value)
            vc = context.new_v()

            context.push_v(vc)
            self.visit(a.value, context)

            # if a.value.type.name == 'Number':
            #     child_context.new_line(
            #         f'{define_v(vn)} = system_copyNumber({vc});')
            # elif a.value.type.name == 'Boolean':
            #     child_context.new_line(
            #         f'{define_v(vn)} = system_copyBoolean({vc});')
            # else:
            #     child_context.new_line(f'{define_v(vn)} = {vc};')
            context.new_line(f'{define_v(vn)} = {vc};')

        self.visit(node.body, context)

        for a in node.assignments:
            del context.dict_v[a.name.value]

    @visitor.when(IfNode)
    def visit(self, node: IfNode, context: GeneratorContext):
        vr = context.pop_v()
        context.new_line(f'{define_v(vr)};')

        l = [(node.condition, node.body)]+[(i.condition, i.body)
                                           for i in node.elif_clauses]

        for i, (c, b) in enumerate(l):
            cond = context.new_v()
            context.push_v(cond)
            self.visit(c, context)

            context.new_line(f'if ({cond})')
            context.new_line('{')

            body = context.new_v()
            context.push_v(body)
            self.visit(b, context)

            context.new_line(f'{vr} = {body};')
            context.new_line('}')
            context.new_line('else')
            context.new_line('{')

            if i == len(l)-1:
                body = context.new_v()
                context.push_v(body)
                self.visit(node.else_body, context)

                context.new_line(f'{vr} = {body};')

        for _ in l:
            context.new_line('}')

    @visitor.when(ElifNode)
    def visit(node: ElifNode, context: GeneratorContext):
        pass

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, context: GeneratorContext):
        vr = context.pop_v()
        vc = context.new_v()
        context.new_line(f'{define_v(vr)};')

        cond = context.new_v()
        context.push_v(cond)
        self.visit(node.condition, context)

        context.new_line(f'{define_v(vc)} = {cond};')
        context.new_line(f'while(system_typeToBoolean({vc}))')
        context.new_line('{')

        body = context.new_v()
        context.push_v(body)
        self.visit(node.body, context)

        context.new_line(f'{vr} = {body};')

        cond = context.new_v()
        context.push_v(cond)
        self.visit(node.condition, context)

        context.new_line(f'{vc} = {cond};')

        context.new_line('}')

    @visitor.when(ForNode)
    def visit(self, node: ForNode, context: GeneratorContext):
        vr = context.pop_v()
        context.new_line(f'{define_v(vr)};')

        vi = context.new_v()
        context.push_v(vi)
        self.visit(node.iterable, context)

        v = context.get_v(node.variable.value)

        context.new_line(f'system_reset({vi});')
        context.new_line(f'while(system_typeToBoolean(system_next({vi})))')
        context.new_line('{')

        context.new_line(f'{define_v(v)} = system_current({vi});')

        body = context.new_v()
        context.push_v(body)

        self.visit(node.body, context)
        context.new_line(f'{vr} = {body};')

        context.new_line('}')

    @visitor.when(ArrayCallNode)
    def visit(self, node: ArrayCallNode, context: GeneratorContext):
        vec = context.new_v()
        context.push_v(vec)

        self.visit(node.expression, context)

        index = context.new_v()
        context.push_v(index)

        self.visit(node.indexer, context)

        context.new_line(
            f'{define_v(context.pop_v())} = system_get({vec}, {index});')
        
    @visitor.when(AssignmentArrayNode)
    def visit(self,node:AssignmentArrayNode,context:GeneratorContext):
        vec = context.new_v()
        context.push_v(vec)

        self.visit(node.array_call.expression, context)

        index = context.new_v()
        context.push_v(index)

        self.visit(node.array_call.indexer, context)

        value = context.new_v()
        context.push_v(value)

        self.visit(node.value, context)

        context.new_line(
            f'{define_v(context.pop_v())} = system_set({vec}, {index}, {value});')
        


def load_c_tools() -> str:
    f = open("src/c_tools/c_tools.c", "r")
    c = f.read()
    f.close()

    return c.split("// FINISH C TOOLS")[0]


def hulk_code_generator(ast: ASTNode):
    c_tools = load_c_tools()

    generator = HulkCodeGenerator()

    code = c_tools+'\n'+generator.visit(ast)

    f = open('cache/main.c', 'w')
    f.write(code)
    f.close()
