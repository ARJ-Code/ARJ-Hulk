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
                    self.errors.append(f'Circular inheritance detected in class {t.name}')
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
                    self.errors.append(f'Circular inheritance detected in protocol {p.name}')
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
        for statement in node.first_is:
            self.visit(statement)
        for statement in node.second_is:
            self.visit(statement)
        
        self.check_circular_inheritance()

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode):
        def _build_attribute(param: ParameterNode):
            p_type = self.visit(param)
            return Attribute(param.name.value, p_type)

        try:
            parameters: List[Attribute] = [_build_attribute(param) for param in node.parameters]
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
            parameters: List[Attribute] = [_build_attribute(param) for param in node.parameters]
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
        params: List[Attribute] = [self.visit(param) for param in node.parameters]
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
            parameters: List[Attribute] = [_build_attribute(param) for param in node.parameters]
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
        # for statement in node.first_is:
        #     self.visit(statement, scope)
        # for statement in node.second_is:
        #     self.visit(statement, scope)
        program_node = self.graph.add_node()
        self.graph.add_path(program_node, self.visit(node.expression, scope))
        try: 
            self.graph.type_inference()
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        let_node = self.graph.add_node()
        for assignment in node.assignments:
            self.visit(assignment, scope)
        return self.graph.add_path(let_node, self.visit(node.body, scope.create_child_scope()))

    @visitor.when(DeclarationNode)
    def visit(self, node: DeclarationNode, scope: Scope):
        var_type = self.visit(node.type, scope)
        var_node = self.graph.add_node(var_type)
        scope.define_variable(node.name, var_node)
        self.graph.add_path(var_node, self.visit(node.value, scope.create_child_scope()))

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope: Scope):
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
