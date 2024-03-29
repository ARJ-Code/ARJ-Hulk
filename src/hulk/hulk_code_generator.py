from .hulk_ast import *
import compiler_tools.visitor as visitor
from typing import Dict, List
from .hulk_defined import is_defined_method
from .hulk_semantic_check import Context


def define_v(v: str):
    return f'Type *{v}'


def new_number(v: str):
    return f'system_createNumber({v})'


def new_boolean(v: str):
    return f'system_createBoolean({v})'


def new_string(v: str):
    return f'system_createString({v})'


class GeneratorContext:
    def __init__(self, parent: 'GeneratorContext | None' = None):
        self.parent: 'GeneratorContext | None' = parent
        self.dict_v: Dict[str, str] = {}
        self.curr_v: int = 0
        self.indentation: int = 0
        self.code: List[str] = []
        self.stack_v: List[str] = []

    def new_line(self, line: str):
        if self.parent is not None:
            self.parent.new_line(line)
            return
        if line == '}':
            self.indentation -= 1

        tabs = '\t'*self.indentation

        self.code.append(tabs+line)
        if line == '{':
            self.indentation += 1

    def new_v(self) -> str:
        if self.parent is not None:
            return self.parent.new_v()

        v = 'v'+str(self.curr_v)
        self.curr_v += 1
        return v

    def define_v(self, v) -> str:
        self.dict_v[v] = self.new_v()

        return self.dict_v[v]

    def get_v(self, v: str) -> str | None:
        if v in self.dict_v:
            return self.dict_v[v]

        if self.parent is not None:
            return self.parent.get_v(v)

        return None

    def get_code(self):
        if self.parent is not None:
            return self.parent.get_code()

        return '\n'.join(l for l in self.code)

    def push_v(self, v: str):
        if self.parent is not None:
            self.parent.push_v(v)
            return

        self.stack_v.append(v)

    def pop_v(self) -> str:
        if self.parent is not None:
            return self.parent.pop_v()

        v = self.stack_v[-1]
        self.stack_v.pop()

        return v

    def top_v(self) -> str:
        return self.stack_v[-1]

    def child(self) -> 'GeneratorContext':
        return GeneratorContext(self)


class GeneratorProgram:
    def __init__(self) -> None:
        self.functions: List[GeneratorContext] = []
        self.declarations: List[str] = []

    def new_function(self) -> GeneratorContext:
        context = GeneratorContext()
        self.functions.append(context)
        return context

    def new_declaration(self, code: str):
        self.declarations.append(code)

    def load_c_tools(self) -> str:
        f = open("src/c_tools/c_tools.c", "r")
        c = f.read()
        f.close()

        return c.split("// FINISH C TOOLS")[0]

    def get_code(self) -> str:
        code = self.load_c_tools()
        declarations = '\n\n'.join(d for d in self.declarations)
        functions = '\n\n'.join(f.get_code() for f in self.functions)

        return f'{code}\n\n{declarations}\n\n{functions}'


class HulkCodeGenerator(object):
    def __init__(self, semantic_context: Context):
        self.generator_program: GeneratorProgram = GeneratorProgram()
        self.semantic_context: Context = semantic_context
        self.type_to_int: Dict[str, int] = {}

    def generate_graph(self) -> List[str]:
        adj = []

        context = GeneratorContext()
        context.indentation=1

        for k in self.semantic_context.types.keys():
            adj.append([])
            self.type_to_int[k] = len(self.type_to_int)

        for k in self.semantic_context.protocols.keys():
            adj.append([])
            self.type_to_int[k] = len(self.type_to_int)

        for k, v in self.semantic_context.types.items():
            if v.parent is not None:
                adj[self.type_to_int[k]].append(
                    self.type_to_int[v.parent.name])

            for p in v.protocols:
                adj[self.type_to_int[k]].append(self.type_to_int[p.name])

        context.new_line(f'system_graph = malloc(sizeof(int*)*{len(adj)});')

        for i in range(len(adj)):
            context.new_line(
                f'system_graph[{i}] = malloc(sizeof(int)*{len(adj[i])+1});')
            context.new_line(f'system_graph[{i}][0] = {len(adj[i])};')

            for j in range(len(adj[i])):
                context.new_line(f'system_graph[{i}][{j+1}] = {adj[i][j]};')

        return context.code

    def get_code(self) -> str:
        return self.generator_program.get_code()

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        graph = self.generate_graph()

        for i in node.first_is:
            self.visit(i)
        for i in node.second_is:
            self.visit(i)

        main_context = self.generator_program.new_function()

        main_context.new_line('int main()')
        main_context.new_line('{')
        main_context.new_line('srand48(time(NULL));')

        main_context.code += graph

        main_context.new_line('\n\t// main tools\n')

        main_context.push_v(main_context.new_v())
        self.visit(node.expression, main_context)

        main_context.new_line('}')

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

        fc = 'system' if is_defined_method(node.name.value) else 'global'

        context.new_line(
            f'{define_v(context.pop_v())} = {fc}_{node.name.value}({params});')

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

    @visitor.when(ExpressionBlockNode)
    def visit(self, node: ExpressionBlockNode, context: GeneratorContext):
        for n in node.instructions[:-1]:
            v = context.new_v()
            context.push_v(v)
            self.visit(n, context)

        self.visit(node.instructions[-1], context)

    @visitor.when(LetNode)
    def visit(self, node: LetNode, context: GeneratorContext):
        for a in node.assignments:
            vc = context.new_v()
            context.push_v(vc)

            self.visit(a.value, context)

            context = context.child()
            vn = context.define_v(a.name.value)
            context.new_line(f'{define_v(vn)} = {vc};')

        self.visit(node.body, context)

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

            context.new_line(f'if (system_typeToBoolean({cond}))')
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

        context = context.child()
        v = context.define_v(node.variable.value)

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
    def visit(self, node: AssignmentArrayNode, context: GeneratorContext):
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

    @visitor.when(AssignmentPropertyNode)
    def visit(self, node: AssignmentPropertyNode, context: GeneratorContext):
        v = context.new_v()
        context.push_v(v)

        self.visit(node.value, context)

        context.new_line(
            f'system_removeEntry({context.get_v("self")}, "p_{node.property.value}");')
        context.new_line(
            f'system_addEntry({context.get_v("self")}, "p_{node.property.value}", {v});')
        context.new_line(f'{define_v( context.pop_v())} = {v};')

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode):
        context = self.generator_program.new_function()

        declaration = f'Type *global_{node.name.value}({", ".join(f"Type *{context.define_v(p.name.value)}" for p in node.parameters)});'
        self.generator_program.new_declaration(declaration)

        context.new_line(declaration[:-1])
        context.new_line('{')

        vr = context.new_v()
        context.push_v(vr)

        self.visit(node.body, context)

        context.new_line(f'return {vr};')
        context.new_line('}')

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        functions = self.semantic_context.get_type(
            node.class_type.name).all_methods()

        create_context = self.generator_program.new_function()
        attributes_context = self.generator_program.new_function()

        parameters = [] if not isinstance(node.class_type, ClassTypeParameterNode) else [
            p.name.value for p in node.class_type.parameters]

        declaration_c = f'Type *create_{node.class_type.name.value}({", ".join(f"Type *{create_context.define_v(p)}" for p in parameters)});'

        ct = attributes_context.new_v()
        declaration_a = f'void attributes_{node.class_type.name.value}(Type *{ct}{", " if len(parameters)!=0 else ""}{", ".join(f"Type *{attributes_context.define_v(p)}" for p in parameters)});'

        self.generator_program.new_declaration(declaration_c)
        self.generator_program.new_declaration(declaration_a)

        attributes_context.new_line(declaration_a[:-1])
        attributes_context.new_line('{')

        for i in node.body:
            if not isinstance(i, ClassPropertyNode):
                continue
            v = attributes_context.new_v()
            attributes_context.push_v(v)

            self.visit(i.expression, attributes_context)
            attributes_context.new_line(
                f'system_addEntry({ct}, "p_{i.name.value}", {v});')

        if isinstance(node.inheritance, InheritanceNode):
            if isinstance(node.inheritance, InheritanceParameterNode):
                parameters_ih = []

                for p in node.inheritance.parameters:
                    v = attributes_context.new_v()
                    attributes_context.push_v(v)
                    self.visit(p, attributes_context)
                    parameters_ih.append(v)

                attributes_context.new_line(
                    f'attributes_{node.inheritance.name.value}({ct}{"" if len(parameters_ih)==0 else ", "}{", ".join(parameters_ih)});')
            else:
                attributes_context.new_line(
                    f'attributes_{node.inheritance.name.value}({ct});')

        attributes_context.new_line('}')

        create_context.new_line(declaration_c[:-1])
        create_context.new_line('{')

        ct = create_context.new_v()
        create_context.new_line(f'Type *{ct} = system_createType();')

        for f, t in functions:
            if f.name == 'init':
                continue
            create_context.new_line(
                f'system_addEntry({ct}, "f_{f.name}", *type_{t.name}_{f.name});')

        create_context.new_line(f'system_addEntry({ct}, "type", "{t.name}");')

        q=create_context.new_v()
        create_context.new_line(f'int *{q} =  malloc(sizeof(int));')
        create_context.new_line(f'*{q} =  {self.type_to_int[t.name]};')

        create_context.new_line(
            f'system_addEntry({ct}, "type_ind", {q});')

        create_context.new_line(
            f'attributes_{node.class_type.name.value}({ct}{", " if len(parameters)!=0 else ""}{", ".join(create_context.get_v(p) for p in parameters)});')

        create_context.new_line(f'return {ct};')
        create_context.new_line('}')

        for i in node.body:
            if not isinstance(i, ClassFunctionNode):
                continue
            self.visit(i, node.class_type.name.value)

    @visitor.when(IsNode)
    def visit(self,node:IsNode,context:GeneratorContext):
        v=context.new_v()
        context.push_v(v)

        self.visit(node.expression,context)

        ind=context.new_v()
        context.new_line(f'int *{ind} = system_findEntry({v}, "type_ind");')

        context.new_line(f'{define_v(context.pop_v())} = system_createBoolean(system_search_type(*{ind}, {self.type_to_int[node.type_name.value]}));')

    @visitor.when(ClassFunctionNode)
    def visit(self, node: ClassFunctionNode, t_name: str):
        context = self.generator_program.new_function()

        ct = context.define_v('self')

        declaration = f'Type *type_{t_name}_{node.name.value}(Type *{ct}{", " if len(node.parameters)!=0 else ""}{", ".join(f"Type *{context.define_v(p.name.value)}" for p in node.parameters)});'
        self.generator_program.new_declaration(declaration)

        context.new_line(declaration[:-1])
        context.new_line('{')

        vr = context.new_v()
        context.push_v(vr)

        self.visit(node.body, context)

        context.new_line(f'return {vr};')
        context.new_line('}')

    @visitor.when(InstancePropertyNode)
    def visit(self, node: InstancePropertyNode, context: GeneratorContext):
        context.new_line(
            f'{define_v(context.pop_v())} = system_findEntry({context.get_v("self")}, "p_{node.property.value}");')

    @visitor.when(InstanceFunctionNode)
    def visit(self, node: InstanceFunctionNode, context: GeneratorContext):
        v = context.new_v()
        context.push_v(v)

        self.visit(node.expression, context)

        f = context.new_v()
        context.new_line(
            f'Type *(*{f})({", ".join("Type *" for _ in range(len(node.property.parameters)+1))}) = system_findEntry({v}, "f_{node.property.name.value}");')

        vp = []

        for p in node.property.parameters:
            aux = context.new_v()
            context.push_v(aux)
            vp.append(aux)

            self.visit(p, context)

        params = f'{v}{", "if len(node.property.parameters)!=0 else ""}{", ".join(vp)}'

        context.new_line(
            f'{define_v(context.pop_v())} = {f}({params});')

    @visitor.when(NewNode)
    def visit(self, node: NewNode, context: GeneratorContext):
        vp = []

        for p in node.name.parameters:
            aux = context.new_v()
            context.push_v(aux)
            vp.append(aux)

            self.visit(p, context)

        params = ', '.join(vp)

        context.new_line(
            f'{define_v(context.pop_v())} = create_{node.name.name.value}({params});')


def hulk_code_generator(ast: ASTNode, semantic_context: Context):
    generator = HulkCodeGenerator(semantic_context)

    generator.visit(ast)
    code = generator.get_code()

    f = open('cache/main.c', 'w')
    f.write(code)
    f.close()
