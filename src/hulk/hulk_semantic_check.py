from compiler_tools import visitor
from hulk.hulk_ast import *
from hulk.hulk_semantic_tools import *
from hulk.hulk_defined import *


class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context: Context = None
        self.errors: List[str] = errors

    @visitor.on('node')
    def visit(self, node: ASTNode):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.context = Context()
        for df in defined_class:
            self.context.add_type(df)
        for dp in defined_protocols:
            self.context.add_protocol(dp)

        for statement in node.first_is:
            self.visit(statement)
        for statement in node.second_is:
            self.visit(statement)

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode):
        self.visit(node.protocol_type)

    @visitor.when(ProtocolTypeNode)
    def visit(self, node: ProtocolTypeNode):
        try:
            self.context.create_protocol(node.name)
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        self.visit(node.class_type)

    @visitor.when(ClassTypeNode)
    def visit(self, node: ClassTypeNode):
        try:
            self.context.create_type(node.name)
        except SemanticError as error:
            self.errors.append(error.text)


class TypeBuilder(object):
    def __init__(self, context, errors=[]):
        self.context: Context = context
        self.current_type: Type = None
        self.errors: List[str] = errors

    def check_circular_inheritance(self) -> None:
        visited: {str, bool} = {}

        for k in self.context.types.keys():
            visited[k] = False
        for t in self.context.types.values():
            s = set()
            while t is not None and not visited[t.name]:
                visited[t.name] = True
                if t in s:
                    self.errors.append(
                        f'Circular inheritance detected in class {t.name}')
                    break
                s.add(t)
                t = t.parent

        visited = {}

        for k in self.context.protocols.keys():
            visited[k] = False
        for p in self.context.protocols.values():
            s = set()
            while p is not None and not visited[p.name]:
                visited[p.name] = True
                if p in s:
                    self.errors.append(
                        f'Circular inheritance detected in protocol {p.name}')
                    break
                s.add(p)
                p = p.parent

    def implement_protocols(self):
        for t in self.context.types.values():
            for p in self.context.protocols.values():
                if t.implement_protocol(p):
                    t.add_protocol(p)

    # def check_overriding(self) -> None:
    #     for t in self.context.types.values():
    #         for method in t.methods:

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for method in defined_methods:
            self.context.add_method(method)

        for statement in node.first_is:
            self.visit(statement)
        for statement in node.second_is:
            self.visit(statement)

        self.check_circular_inheritance()
        self.implement_protocols()

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode):
        def _build_attribute(param: ParameterNode):
            p_type = self.visit(param).type
            return Attribute(param.name.value, p_type)

        try:
            parameters: List[Attribute] = [
                _build_attribute(param) for param in node.parameters]
            return_type = self.visit(node.return_type)
            self.context.create_method(node.name, parameters, return_type)
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode):
        extension_type = self.visit(node.extension)
        self.current_type = self.context.get_protocol(node.protocol_type.name)
        self.current_type.set_parent(extension_type)
        for statement in node.body:
            self.visit(statement)
        self.current_type = None

    @visitor.when(ExtensionNode)
    def visit(self, node: ExtensionNode):
        try:
            return self.context.get_protocol(node.name)
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(ProtocolFunctionNode)
    def visit(self, node: ProtocolFunctionNode) -> Attribute:
        def _build_attribute(param: ParameterNode):
            p_type = self.visit(param)
            return Attribute(param.name.value, p_type)

        try:
            parameters: List[Attribute] = [
                _build_attribute(param) for param in node.parameters]
            return_type = self.visit(node.type)
            self.current_type.define_method(node.name, parameters, return_type)
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        self.visit(node.class_type)
        inheritance_type = self.visit(node.inheritance)
        self.current_type = self.context.get_type(node.class_type.name)
        self.current_type.set_parent(inheritance_type)
        for statement in node.body:
            self.visit(statement)
        self.current_type = None

    @visitor.when(ClassTypeNode)
    def visit(self, node: ClassTypeNode):
        class_type = self.context.get_type(node.name)
        class_type.add_method(Method('init', class_type, []))
        return class_type

    @visitor.when(ClassTypeParameterNode)
    def visit(self, node: ClassTypeParameterNode):
        class_type = self.context.get_type(node.name)
        params: List[Attribute] = [self.visit(
            param) for param in node.parameters]
        for param in params:
            class_type.add_param(param)
        class_type.add_method(Method('init', class_type, params))
        return class_type

    @visitor.when(InheritanceNode)
    def visit(self, node: InheritanceNode):
        try:
            return self.context.get_type(node.name)
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(ClassFunctionNode)
    def visit(self, node: ClassFunctionNode):
        def _build_attribute(param: ParameterNode):
            return self.visit(param)

        try:
            parameters: List[Attribute] = [
                _build_attribute(param) for param in node.parameters]
            return_type = self.visit(node.type)
            self.current_type.define_method(node.name, parameters, return_type)
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(ClassPropertyNode)
    def visit(self, node: ClassPropertyNode):
        try:
            attr_type = self.visit(node.type)
            self.current_type.define_attribute(node.name, attr_type)
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(EOFInheritsNode)
    def visit(self, node: EOFInheritsNode):
        return OBJECT

    @visitor.when(EOFExtensionNode)
    def visit(self, node: EOFExtensionNode):
        return None

    @visitor.when(EOFNode)
    def visit(self, node: EOFNode):
        return None

    @visitor.when(ParameterNode)
    def visit(self, node: ParameterNode):
        p_type = self.visit(node.type)
        attribute: Attribute = Attribute(node.name.value, p_type)
        return attribute

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        try:
            return self.context.get_type(node.name)
        except SemanticError as error:
            self.errors.append(error.text)
            return None

    @visitor.when(VectorTypeNode)
    def visit(self, node: VectorTypeNode):
        try:
            typex = self.context.get_type(node.name)
            vector_type = typex
            for i in range(int(node.dimensions)):
                vector_type = self.context.add_type(vector_t(typex, i+1))
            return vector_type
        except SemanticError as error:
            self.errors.append(error.text)


class SemanticChecker(object):
    def __init__(self, context: Context, errors=[]):
        self.errors: List[str] = errors
        self.context: Context = context
        self.graph = SemanticGraph(context)

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: Scope):
        def add_context_functions():
            for method in self.context.methods.values():
                name: str = method.name
                arguments: List[Attribute] = method.arguments
                return_type: Type = method.return_type
                args = [self.graph.add_node(t)
                        for t in [a.type for a in arguments]]
                function_node = self.graph.add_node(return_type)
                scope.define_function(name, function_node, args)

        def add_context_types():
            def get_functions(methods):
                functions = []
                for method in methods:
                    arguments: List[Attribute] = method.arguments
                    return_type: Type = method.return_type
                    args = [self.graph.add_node(t)
                            for t in [a.type for a in arguments]]
                    function_node = self.graph.add_node(return_type)
                    functions.append(
                        Function(method.name, function_node, args))
                return functions

            for t in self.context.types.values():
                attributes = [Variable(a.name, self.graph.add_node(
                    a.type)) for a in t.attributes]
                scope.define_type(t.name, get_functions(t.methods), attributes)

            for p in self.context.protocols.values():
                scope.define_type(p.name, get_functions(p.methods), [])

        add_context_types()
        add_context_functions()

        for statement in node.first_is:
            self.visit(statement, scope)
        for statement in node.second_is:
            self.visit(statement, scope)

        program_node = self.graph.add_node()
        self.graph.add_path(program_node, self.visit(node.expression, scope))

        if len(self.errors) == 0:
            try:
                self.graph.type_inference()
            except SemanticError as error:
                self.errors.append(error.text)

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode, scope: Scope):
        function_ = scope.get_defined_function(node.name)
        child_scope = scope.create_child_scope()
        for i in range(len(function_.args)):
            param_node: SemanticNode = function_.args[i]
            param: ParameterNode = node.parameters[i]
            child_scope.define_variable(param.name, param_node)
        body_node = self.visit(node.body, child_scope)
        self.graph.add_path(function_.node, body_node)

    @visitor.when(AtomicNode)
    def visit(self, node: AtomicNode, scope: Scope):
        try:
            return scope.get_defined_variable(node.name).node
        except SemanticError as error:
            self.errors.append(error.text)
            return self.graph.add_node()

    @visitor.when(ExpressionCallNode)
    def visit(self, node: ExpressionCallNode, scope: Scope):
        try:
            function_ = scope.get_defined_function(
                node.name).check_valid_params(node.name, node.parameters)
            call_node = self.graph.add_node()
            self.graph.add_path(call_node, function_.node)
            for fa, ca in zip(function_.args, node.parameters):
                self.graph.add_path(fa, self.visit(
                    ca, scope.create_child_scope()))
            return call_node
        except SemanticError as error:
            self.errors.append(error.text)
            return self.graph.add_node()

    @visitor.when(ExpressionBlockNode)
    def visit(self, node: ExpressionBlockNode, scope: Scope):
        expression_block_node = self.graph.add_node()
        for instruction in node.instructions[: len(node.instructions) - 1]:
            self.visit(instruction, scope.create_child_scope())
        last_evaluation_node = self.visit(
            node.instructions[-1], scope.create_child_scope())
        return self.graph.add_path(expression_block_node, last_evaluation_node)

    @visitor.when(ForNode)
    def visit(self, node: ForNode, scope: Scope):
        for_node = self.graph.add_node()
        iterable_expression_node = self.visit(
            node.iterable, scope.create_child_scope())
        iterable_type = iterable_type = self.graph.local_type_inference(
            iterable_expression_node)
        current_type = self.context.get_type(LexerToken(
            0, 0, iterable_type.name, '')).get_method('current').return_type
        variable_node = self.graph.add_node(current_type)
        child_scope = scope.create_child_scope()
        child_scope.define_variable(node.variable, variable_node)
        expression_node = self.visit(node.body, child_scope)
        return self.graph.add_path(for_node, expression_node)

    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope: Scope):
        if_node = self.graph.add_node()
        conditional_node = self.graph.add_node(BOOLEAN)
        self.graph.add_path(self.visit(
            node.condition, scope.create_child_scope()), conditional_node)
        then_node = self.graph.add_node()
        self.graph.add_path(if_node, self.graph.add_path(
            then_node, self.visit(node.body, scope.create_child_scope())))
        for elif_ in node.elif_clauses:
            elif_node = self.graph.add_node()
            self.graph.add_path(elif_node, self.visit(
                elif_, scope.create_child_scope()))
        else_node = self.graph.add_node()
        return self.graph.add_path(if_node, self.graph.add_path(else_node, self.visit(node.else_body, scope.create_child_scope())))

    @visitor.when(ElifNode)
    def visit(self, node: ElifNode, scope: Scope):
        elif_node = self.graph.add_node()
        conditional_node = self.graph.add_node(BOOLEAN)
        self.graph.add_path(self.visit(
            node.condition, scope.create_child_scope()), conditional_node,)
        return self.graph.add_path(elif_node, self.visit(node.body, scope.create_child_scope()))

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        while_node = self.graph.add_node()
        conditional_node = self.graph.add_node(BOOLEAN)
        self.graph.add_path(self.visit(
            node.condition, scope.create_child_scope()), conditional_node)
        return self.graph.add_path(while_node, self.visit(node.body, scope.create_child_scope()))

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        let_node = self.graph.add_node()
        new_scope = scope.create_child_scope()
        for assignment in node.assignments:
            self.visit(assignment, new_scope)
            new_scope = new_scope.create_child_scope()
        return self.graph.add_path(let_node, self.visit(node.body, new_scope))

    @visitor.when(DeclarationNode)
    def visit(self, node: DeclarationNode, scope: Scope):
        expression_node = self.visit(node.value, scope.create_child_scope())
        var_type = self.visit(node.type, scope)
        var_node = self.graph.add_node(var_type)
        scope.define_variable(node.name, var_node)
        self.graph.add_path(var_node, expression_node)

    @visitor.when(AssignmentNode)
    def visit(self, node: AssignmentNode, scope: Scope):
        var_node = scope.get_defined_variable(node.name).node
        expression_node = self.visit(node.value, scope.create_child_scope())
        self.graph.add_path(var_node, expression_node)
        return expression_node

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope: Scope):
        return self.context.get_type(node.name)

    @visitor.when(VectorTypeNode)
    def visit(self, node: VectorTypeNode, scope: Scope):
        type_ = self.context.get_type(node.name)
        vector_type = self.context.add_type(vector_t(type_, node.dimensions))
        node.name.value = (
            f'[{node.name.value}' + (f', {node.dimensions}' if node.dimensions > 1 else '')) + ']'
        return vector_type

    @visitor.when(EOFTypeNode)
    def visit(self, node: EOFTypeNode, scope: Scope):
        return None

    @visitor.when(ConstantNode)
    def visit(self, node: ConstantNode, scope: Scope):
        constant_type = OBJECT
        if node.type == ConstantTypes.STRING:
            constant_type = STRING
        elif node.type == ConstantTypes.BOOLEAN:
            constant_type = BOOLEAN
        else:
            constant_type = NUMBER
        return self.graph.add_node(constant_type)

    @visitor.when(BooleanUnaryNode)
    def visit(self, node: BooleanUnaryNode, scope: Scope):
        expression_node = self.visit(node.child, scope.create_child_scope())
        expression_node.node_type = BOOLEAN
        return expression_node

    @visitor.when(ArithmeticUnaryNode)
    def visit(self, node: ArithmeticUnaryNode, scope: Scope):
        expression_node = self.visit(node.child, scope.create_child_scope())
        expression_node.node_type = NUMBER
        return expression_node

    @visitor.when(BooleanBinaryNode)
    def visit(self, node: BooleanBinaryNode, scope: Scope):
        boolean_node = self.graph.add_node(BOOLEAN)
        is_boolean_operation = node.operator in [
            BooleanOperator.AND, BooleanOperator.OR]
        left_type = BOOLEAN if is_boolean_operation else NUMBER
        left_expression_node = self.visit(
            node.left, scope.create_child_scope())
        left_expression_node.node_type = left_type
        right_type = BOOLEAN if is_boolean_operation else NUMBER
        right_expression_node = self.visit(
            node.right, scope.create_child_scope())
        right_expression_node.node_type = right_type

        return boolean_node

    @visitor.when(ArithmeticBinaryNode)
    def visit(self, node: ArithmeticBinaryNode, scope: Scope):
        number_node = self.graph.add_node(NUMBER)
        left_expression_node = self.visit(
            node.left, scope.create_child_scope())
        left_expression_node.node_type = NUMBER
        right_expression_node = self.visit(
            node.right, scope.create_child_scope())
        right_expression_node.node_type = NUMBER
        return number_node

    @visitor.when(StringBinaryNode)
    def visit(self, node: StringBinaryNode, scope: Scope):
        string_node = self.graph.add_node(STRING)
        obj = self.graph.add_node(OBJECT)
        left_expression_node = self.visit(
            node.left, scope.create_child_scope())
        right_expression_node = self.visit(
            node.right, scope.create_child_scope())
        self.graph.add_path(obj, left_expression_node)
        self.graph.add_path(obj, right_expression_node)
        return string_node

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope):
        scope = scope.create_child_scope()
        init_scope = scope.create_child_scope()

        scope.define_variable(LexerToken(0, 0, 'self', ''), self.graph.add_node(
            self.context.get_type(node.class_type.name)))

        t = scope.get_defined_type(
            node.class_type.name)
        init_f = t.get_function('init')

        if isinstance(node.class_type, ClassTypeParameterNode):
            for p, n in zip(node.class_type.parameters, init_f.args):
                init_scope.define_variable(p.name, n)

        try:
            if isinstance(node.inheritance, InheritanceNode):
                if isinstance(node.inheritance, InheritanceParameterNode):
                    parent = scope.get_defined_type(node.inheritance.name)
                    parent.get_function('init').check_valid_params(
                        node.inheritance.name, node.inheritance.parameters)

                    for p, n in zip(node.inheritance.parameters, parent.get_function('init').args):
                        et = self.visit(p, init_scope)
                        self.graph.add_path(n, et)
                else:
                    parent = scope.get_defined_type(node.inheritance.name)
                    parent.get_function('init').check_valid_params(
                        node.inheritance.name, [])

        except SemanticError as error:
            self.errors.append(error.text)

        for s in node.body:
            if isinstance(s, ClassFunctionNode):
                function_ = t.get_function(s.name.value)
                self.visit(s, function_, scope)
            if isinstance(s, ClassPropertyNode):
                et = self.visit(s.expression, init_scope)
                self.graph.add_path(t.get_attribute(s.name.value).node, et)

    @visitor.when(ClassFunctionNode)
    def visit(self, node: ClassFunctionNode, function_: SemanticNode, scope: Scope):
        child_scope = scope.create_child_scope()
        for i in range(len(function_.args)):
            param_node: SemanticNode = function_.args[i]
            param: ParameterNode = node.parameters[i]
            child_scope.define_variable(param.name, param_node)
        body_node = self.visit(node.body, child_scope)
        self.graph.add_path(function_.node, body_node)

    @visitor.when(ExplicitArrayDeclarationNode)
    def visit(self, node: ExplicitArrayDeclarationNode, scope: Scope):
        VECTOR = Type('Vector')
        vector_node = self.graph.add_node(VECTOR)
        for expression in node.values:
            expression_node = self.visit(
                expression, scope.create_child_scope())
            self.graph.add_path(vector_node, expression_node)
        return vector_node

    @visitor.when(NewNode)
    def visit(self, node: NewNode, scope: Scope):
        try:
            t = scope.get_defined_type(node.name.name)
            init = t.get_function('init')

            init.check_valid_params(node.name.name, node.name.parameters)
            for p, a in zip(node.name.parameters, init.args):
                n = self.visit(p, scope)
                self.graph.add_path(a, n)
        except SemanticError as error:
            self.errors.append(error.text)

        return self.graph.add_node(init.node.node_type)

    @visitor.when(IsNode)
    def visit(self, node: IsNode, scope: Scope):
        boolean = self.graph.add_node(BOOLEAN)

        try:
            scope.get_defined_type(node.type_name)
        except SemanticError as error:
            self.errors.append(error.text)

        self.visit(node.expression, scope)
        return boolean

    @visitor.when(ImplicitArrayDeclarationNode)
    def visit(self, node: ImplicitArrayDeclarationNode, scope: Scope):
        try:
            VECTOR = Type('Vector')
            vector_node = self.graph.add_node(VECTOR)
            iterable_node = self.visit(
                node.iterable, scope.create_child_scope())
            iterable_type = self.graph.local_type_inference(iterable_node)
            current_type = self.context.get_type(LexerToken(
                0, 0, iterable_type.name, '')).get_method('current').return_type
            item_node = self.graph.add_node(current_type)
            child_scope = scope.create_child_scope()
            child_scope.define_variable(node.item, item_node)
            expression_node = self.visit(node.expression, child_scope)
            self.graph.add_path(item_node, expression_node)
            return self.graph.add_path(vector_node, expression_node)
        except SemanticError as error:
            self.errors.append(error.text)
            return self.graph.add_node()

    @visitor.when(ArrayCallNode)
    def visit(self, node: ArrayCallNode, scope: Scope):
        index_node = self.graph.add_node(NUMBER)
        index_expression_node = self.visit(
            node.indexer, scope.create_child_scope())
        self.graph.add_path(index_expression_node, index_node)
        indexable_get_expression_node = self.visit(
            node.expression, scope.create_child_scope())
        getable_type = self.graph.local_type_inference(
            indexable_get_expression_node)
        get_type = self.context.get_type(LexerToken(
            0, 0, getable_type.name, '')).get_method('get').return_type
        return self.graph.add_node(get_type)

    @visitor.when(AssignmentArrayNode)
    def visit(self, node: AssignmentArrayNode, scope: Scope):
        index_node = self.graph.add_node(NUMBER)
        index_expression_node = self.visit(
            node.array_call.indexer, scope.create_child_scope())
        self.graph.add_path(index_expression_node, index_node)
        indexable_set_expression_node = self.visit(
            node.array_call.expression, scope.create_child_scope())
        set_expression_node = self.visit(
            node.value, scope.create_child_scope())
        setable_type = self.graph.local_type_inference(
            indexable_set_expression_node)
        set_type = scope.get_type(LexerToken(
            0, 0, setable_type.name, '')).get_method('set').arguments[1].type
        set_node = self.graph.add_node(set_type)
        return self.graph.add_path(set_expression_node, set_node)

    @visitor.when(InstancePropertyNode)
    def visit(self, node: InstancePropertyNode, scope: Scope):
        try:
            var_node = scope.get_defined_variable(node.name)
            p_type = self.graph.local_type_inference(
                var_node.node)
            r_type = scope.get_defined_type(LexerToken(
                0, 0, p_type.name, '')).get_attribute(node.property.value).node
            return r_type
        except SemanticError as error:
            self.errors.append(error.text)
            return self.graph.add_node()

    @visitor.when(AssignmentPropertyNode)
    def visit(self, node: AssignmentPropertyNode, scope: Scope):
        try:
            var_node = scope.get_defined_variable(node.name)
            v_type = self.graph.local_type_inference(
                var_node.node)
            p_type = scope.get_defined_type(LexerToken(
                0, 0, v_type.name, '')).get_attribute(node.property.value).node
            r_type = self.visit(node.value, scope)
            self.graph.add_path(p_type, r_type)
            return r_type
        except SemanticError as error:
            self.errors.append(error.text)
            return self.graph.add_node()

    @visitor.when(InstanceFunctionNode)
    def visit(self, node: InstanceFunctionNode, scope: Scope):
        try:
            e_node = self.visit(node.expression, scope)
            e_type = self.graph.local_type_inference(e_node)
            function_ = scope.get_defined_type(LexerToken(
                0, 0, e_type.name, '')).get_function(node.property.name.value)
            function_.check_valid_params(LexerToken(
                0, 0, '', ''), node.property.parameters)

            for fa, ca in zip(function_.args, node.property.parameters):
                self.graph.add_path(fa, self.visit(ca, scope))

            return function_.node
        except SemanticError as error:
            self.errors.append(error.text)
            return self.graph.add_node()


def hulk_semantic_check(ast: ASTNode) -> SemanticResult:
    errors = []

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    scope = Scope()

    semantic_checker = SemanticChecker(context, errors)
    semantic_checker.visit(ast, scope)

    return SemanticResult(context, errors)
