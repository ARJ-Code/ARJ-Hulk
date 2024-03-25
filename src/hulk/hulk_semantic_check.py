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
        # for df in defined_class:
        #     self.context.add_type(df)
        # for dp in defined_protocols:
        #     self.context.add_type(dp)

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


# class HierarchicalInfererVisitor(object):
#     def __init__(self) -> None:

#     @visitor.on('node')
#     def visit(self, node: ASTNode, scope: Scope):
#         pass
    
#     @visitor.when(ProgramNode)
#     def visit(self, node: ProgramNode, scope: Scope):
#         for statement in node.first_is:
#             self.visit(statement, scope)
#         for statement in node.second_is:
#             self.visit(statement, scope)

#     @visitor.when(ProtocolDeclarationNode)
#     def visit(self, node: ProtocolDeclarationNode, scope: Scope):
#         p1: Protocol = scope.get_defined_type(node.protocol_type.name)
#         p2: Protocol = scope.get_defined_type(node.extension.name)
#         assert p1 is not None, f'Protocol {node.protocol_type.name} not defined'

#         p1.define_extends(p2)

#         for statement in node.body:
#             assert p1.get_attribute(statement.name) is None, f'Function {statement.name} already defined'

#             self.visit(statement, scope.create_child_scope())
#             p1.add_method(Method(statement.name, statement.params, statement.return_type))
    
#     @visitor.when(ProtocolFunctionNode)
#     def visit(self, node: ProtocolFunctionNode, scope: Scope):
#         for param in node.params:
#             self.visit(param, scope)
#         self.visit(node.type, scope)


#     @visitor.when(ProtocolTypeNode)
#     def visit(self, node: ProtocolTypeNode, scope: Scope):
#         scope.define_protocol(Protocol(node.name))

#     @visitor.when(ClassDeclarationNode)
#     def visit(self, node: ClassDeclarationNode, scope: Scope):
#         self.visit(node.class_type, scope)

#     @visitor.when(ClassTypeNode)
#     def visit(self, node: ClassTypeNode, scope: Scope):
#         scope.define_class(Class(node.name))


# class SemanticCheckerVisitor(object):
#     def __init__(self):
#         self.errors = []
    
#     @visitor.on('node')
#     def visit(self, node, scope):
#         pass
    
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
