from compiler_tools import visitor
from hulk.hulk_ast import *
from hulk.hulk_semantic_tools import *
from hulk.hulk_defined import *
from typing import Tuple


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

    def check_circular_inheritance(self):
        for t in self.context.types.values():
            s = set()
            while t is not None:
                if t in s:
                    self.errors.append(f'Circular inheritance detected in class {t.name}')
                    break
                s.add(t)
                t = t.parent

        for p in self.context.protocols.values():
            s = set()
            while p is not None:
                if p in s:
                    self.errors.append(f'Circular inheritance detected in protocol {p.name}')
                    break
                s.add(p)
                p = p.parent


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
            p_type = self.visit(param)
            return Attribute(param.name.value, p_type)

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
            
class SemanticCheckerVisitor(object):
    def __init__(self):
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
#     @visitor.when(ProgramNode)
#     def visit(self, node: ProgramNode, scope=None):
#         for statement in node.statements:
#             self.visit(statement, scope)
    
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
