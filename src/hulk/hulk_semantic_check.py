from compiler_tools import visitor
from hulk.hulk_ast import *
from hulk.hulk_semantic_tools import *


class TypeRecolectorVisitor(object):
    @visitor.on('node')
    def visit(self, node: ASTNode, scope: Scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: Scope):
        for statement in node.first_is:
            self.visit(statement, scope)
        for statement in node.second_is:
            self.visit(statement, scope)

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode, scope: Scope):
        self.visit(node.protocol_type, scope)

    @visitor.when(ProtocolTypeNode)
    def visit(self, node: ProtocolTypeNode, scope: Scope):
        scope.define_protocol(Protocol(node.name))

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope):
        self.visit(node.class_type, scope)

    @visitor.when(ClassTypeNode)
    def visit(self, node: ClassTypeNode, scope: Scope):
        scope.define_class(Class(node.name))

