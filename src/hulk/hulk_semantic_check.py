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
        self.graph = SemanticGraph()

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
            function_ = scope.check_valid_params(node.name, node.parameters)
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

    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope: Scope):
        if_node = self.graph.add_node()
        conditional_node = self.graph.add_node(BOOLEAN)
        self.graph.add_path(conditional_node, self.visit(
            node.condition, scope.create_child_scope()))
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
        self.graph.add_path(conditional_node, self.visit(
            node.condition, scope.create_child_scope()))
        return self.graph.add_path(elif_node, self.visit(node.body, scope.create_child_scope()))

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        while_node = self.graph.add_node()
        conditional_node = self.graph.add_node(BOOLEAN)
        self.graph.add_path(conditional_node, self.visit(
            node.condition, scope.create_child_scope()))
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
        node.name.value = (
            f'[{node.name.value}' + (f', {node.dimensions}' if node.dimensions > 1 else '')) + ']'
        return self.context.get_type(node.name)

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
        boolean_node = self.graph.add_node(BOOLEAN)
        expression_node = self.visit(node.child, scope.create_child_scope())
        return self.graph.add_path(boolean_node, expression_node)

    @visitor.when(ArithmeticUnaryNode)
    def visit(self, node: ArithmeticUnaryNode, scope: Scope):
        number_node = self.graph.add_node(NUMBER)
        expression_node = self.visit(node.child, scope.create_child_scope())
        return self.graph.add_path(number_node, expression_node)

    @visitor.when(BooleanBinaryNode)
    def visit(self, node: BooleanBinaryNode, scope: Scope):
        boolean_node = self.graph.add_node(BOOLEAN)
        is_boolean_operation = node.operator in [
            BooleanOperator.AND, BooleanOperator.OR]
        left_node = self.graph.add_node(
            BOOLEAN if is_boolean_operation else NUMBER)
        left_expression_node = self.visit(
            node.left, scope.create_child_scope())
        self.graph.add_path(left_node, left_expression_node)
        right_node = self.graph.add_node(
            BOOLEAN if is_boolean_operation else NUMBER)
        right_expression_node = self.visit(
            node.right, scope.create_child_scope())
        self.graph.add_path(right_node, right_expression_node)
        return boolean_node

    @visitor.when(ArithmeticBinaryNode)
    def visit(self, node: ArithmeticBinaryNode, scope: Scope):
        boolean_node = self.graph.add_node(NUMBER)
        left_node = self.graph.add_node(NUMBER)
        left_expression_node = self.visit(
            node.left, scope.create_child_scope())
        self.graph.add_path(left_node, left_expression_node)
        right_node = self.graph.add_node(NUMBER)
        right_expression_node = self.visit(
            node.right, scope.create_child_scope())
        self.graph.add_path(right_node, right_expression_node)
        return boolean_node

    @visitor.when(StringBinaryNode)
    def visit(self, node: StringBinaryNode, scope: Scope):
        string_node = self.graph.add_node(STRING)
        left_node = self.graph.add_node(OBJECT)
        left_expression_node = self.visit(
            node.left, scope.create_child_scope())
        self.graph.add_path(left_node, left_expression_node)
        right_node = self.graph.add_node(OBJECT)
        right_expression_node = self.visit(
            node.right, scope.create_child_scope())
        self.graph.add_path(right_node, right_expression_node)
        return string_node

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope):
        scope = scope.create_child_scope()
        # scope.define_variable(LexerToken(0, 0, 'self', ''), self.graph.add_node(
        #     node_type=self.context.get_type(LexerToken(node.class_type.name))))

        # if isinstance(node.inheritance, InheritanceParameterNode):
        #     parent = scope.get_defined_type(node.inheritance.name)


    # @visitor.when(VarDeclarationNode)
    # def visit(self, node: VarDeclarationNode, scope: Scope):
    #     if scope.is_var_defined(node.id, len(scope.local_vars)):
    #         self.errors.append(f'Variable {node.id} already defined')
    #     else:
    #         scope.define_variable(node.id)
    #         self.visit(node.expr, scope)

    # @visitor.when(FuncDeclarationNode)
    # def visit(self, node: FuncDeclarationNode, scope: Scope):
    #     if scope.is_func_defined(node.id, len(scope.local_funcs)):
    #         self.errors.append(f'Function {node.id}/{len(node.params)} already defined')
    #     else:
    #         scope.define_function(node.id, node.params)
    #         child_scope = scope.create_child_scope()
    #         for param in node.params:
    #             child_scope.define_variable(param)
    #         self.visit(node.body, child_scope)

    # @visitor.when(PrintNode)
    # def visit(self, node: PrintNode, scope: Scope):
    #     self.visit(node.expr, scope)

    # @visitor.when(ConstantNumNode)
    # def visit(self, node: ConstantNumNode, scope: Scope):
    #     pass

    # @visitor.when(VariableNode)
    # def visit(self, node: VariableNode, scope: Scope):
    #     if not scope.is_var_defined(node.lex, len(scope.local_vars)):
    #         self.errors.append(f'Variable {node.lex} not defined')

    # @visitor.when(CallNode)
    # def visit(self, node: CallNode, scope: Scope):
    #     if not scope.is_func_defined(node.lex, len(scope.local_funcs)):
    #         self.errors.append(f'Function {node.lex}/{len(node.args)} not defined')
    #     for arg in node.args:
    #             self.visit(arg, scope)

    # @visitor.when(BinaryNode)
    # def visit(self, node: BinaryNode, scope: Scope):
    #     self.visit(node.left, scope)
    #     self.visit(node.right, scope)
