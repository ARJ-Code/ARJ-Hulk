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
            self.dict_v[v] = self.new_v

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

        context.push_v(context.new_v())
        self.visit(node.expression, context)

        context.new_line('}')

        return context.get_code()

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

    @visitor.when(ConstantNode)
    def visit(self, node: ConstantNode, context: GeneratorContext):
        if node.type == ConstantTypes.BOOLEAN:
            context.new_line(
                f'{define_v(context.pop_v())} = system_createBoolean({node.value.value});')
        if node.type == ConstantTypes.STRING:
            context.new_line(
                f'{define_v(context.pop_v())} = system_createString({node.value.value});')
        if node.type == ConstantTypes.NUMBER:
            context.new_line(
                f'{define_v(context.pop_v())} = system_createNumber({node.value.value});')

    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, context: GeneratorContext):
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


def load_c_tools() -> str:
    f = open("src/c_tools/c_tools.c", "r")
    c = f.read()
    f.close()

    return c.split("// FINISH C TOOLS")[0]


def hulk_code_generator(ast: ASTNode):
    c_tools = load_c_tools()

    generator = HulkCodeGenerator()
    print(generator.visit(ast))
