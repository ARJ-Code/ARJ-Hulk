from abc import ABC
from enum import Enum
from typing import List
from .hulk_semantic_tools import Type
from compiler_tools.lexer import LexerToken

# level 0


class ASTNode (ABC):
    pass

# level 1


class ProgramNode(ASTNode):
    def __init__(self, first_is, expression, second_is):
        self.first_is: List[InstructionNode] = first_is
        self.expression: ExpressionNode = expression
        self.second_is: List[InstructionNode] = second_is


class InstructionNode (ASTNode):
    pass


class ExpressionNode (ASTNode):
    def define_type(self, value: Type):
        self.type = value


class TypeNode (ASTNode):
    def __init__(self, name):
        self.name: LexerToken = name


class VectorTypeNode (TypeNode):
    def __init__(self, name: str, dimensions: LexerToken | None):
        super().__init__(name)
        self.dimensions = 1 if dimensions is None else dimensions.value


class ParameterNode(ASTNode):
    def __init__(self, name, type):
        self.name = name
        self.type: TypeNode = type


class EOFNode (ASTNode):
    pass


class EOFExtensionNode(EOFNode):
    pass


class EOFTypeNode(EOFNode):
    pass


class ProtocolTypeNode(ASTNode):
    def __init__(self, name):
        self.name: LexerToken = name


class ClassTypeNode(ASTNode):
    def __init__(self, name):
        self.name: LexerToken = name


class ClassTypeParameterNode(ClassTypeNode):
    def __init__(self, name, parameters):
        super().__init__(name)
        self.parameters: List[ParameterNode] = parameters


class ExtensionNode(ASTNode):
    def __init__(self, name):
        self.name: LexerToken = name


class InheritanceNode(ASTNode):
    def __init__(self, name):
        self.name: LexerToken = name


class InheritanceParameterNode(InheritanceNode):
    def __init__(self, name, parameters):
        super().__init__(name)
        self.parameters: List[ExpressionNode] = parameters


# level 2
class BinaryNode (ExpressionNode):
    def __init__(self, left, right):
        self.left: ExpressionNode = left
        self.right: ExpressionNode = right


class UnaryNode (ExpressionNode):
    def __init__(self, child):
        self.child: ExpressionNode = child


class AtomicNode(ExpressionNode):
    def __init__(self, name):
        self.name: LexerToken = name


class InstancePropertyNode(AtomicNode):
    def __init__(self, name, p_name):
        super().__init__(name)
        self.property: LexerToken = p_name


class InstanceFunctionNode(ExpressionNode):
    def __init__(self, expression: ExpressionNode, expression_call: 'ExpressionCallNode'):
        self.property: ExpressionCallNode = expression_call
        self.expression: ExpressionNode = expression


class ExpressionCallNode (AtomicNode):
    def __init__(self, name, parameters):
        super().__init__(name)
        self.parameters: List[ExpressionNode] = parameters


class ArrayCallNode(ExpressionNode):
    def __init__(self, expression: ExpressionNode, indexer: ExpressionNode):
        self.expression: ExpressionNode = expression
        self.indexer: ExpressionNode = indexer


class ConstantNode (AtomicNode):
    def __init__(self, value, v_type):
        super().__init__(value)
        self.value: LexerToken = value
        self.type: ConstantTypes = v_type


class StringBinaryNode (BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator: StringOperator = operator


class ArithmeticBinaryNode (BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator: ArithmeticOperator = operator


class ArithmeticUnaryNode (UnaryNode):
    def __init__(self, child, operator):
        super().__init__(child)
        self.operator: ArithmeticOperator = operator


class BooleanBinaryNode (BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator: BooleanOperator = operator


class BooleanUnaryNode (UnaryNode):
    def __init__(self, child, operator):
        super().__init__(child)
        self.operator: BooleanOperator = operator


class ImplicitArrayDeclarationNode (ExpressionNode):
    def __init__(self, expression, variable, iterable):
        self.expression: ExpressionNode = expression
        self.variable: LexerToken = variable
        self.iterable: ExpressionNode = iterable


class ExplicitArrayDeclarationNode(ExpressionNode):
    def __init__(self, values: List[ExpressionNode]):
        self.values: List[ExpressionNode] = values


class FunctionDeclarationNode (InstructionNode):
    def __init__(self, name, parameters, return_type, body):
        self.name: LexerToken = name
        self.parameters: List[ParameterNode] = parameters
        self.return_type: LexerToken = return_type
        self.body: ExpressionNode = body


class ProtocolDeclarationNode(InstructionNode):
    def __init__(self, protocol_type, extension, body):
        self.protocol_type: ProtocolTypeNode = protocol_type
        self.extension: ExtensionNode = extension
        self.body: List[InstructionNode] = body


class ClassDeclarationNode(InstructionNode):
    def __init__(self, class_type, inheritance, body):
        self.class_type: ClassTypeNode = class_type
        self.inheritance: InheritanceNode = inheritance
        self.body: List[TypedInstructionNode] = body


class TypedInstructionNode(ASTNode):
    def __init__(self, name: LexerToken) -> None:
        self.name: LexerToken = name


class ClassInstructionNode(TypedInstructionNode):
    pass


class ProtocolInstructionNode(TypedInstructionNode):
    pass


class ProtocolFunctionNode(ProtocolInstructionNode):
    def __init__(self, name, parameters, p_type):
        super().__init__(name)
        self.parameters: List[ParameterNode] = parameters
        self.type: TypeNode = p_type


class ClassFunctionNode(ClassInstructionNode):
    def __init__(self, name, parameters, p_type, body):
        super().__init__(name)
        self.parameters: List[ParameterNode] = parameters
        self.type: TypeNode = p_type
        self.body: ExpressionNode = body


class ClassPropertyNode(ClassInstructionNode):
    def __init__(self, name, p_type, expression):
        super().__init__(name)
        self.type: TypeNode = p_type
        self.expression: ExpressionNode = expression


class IsNode(ExpressionNode):
    def __init__(self, name, type_name):
        self.name: LexerToken = name
        self.type_name: TypeNode = type_name


class AsNode(ExpressionNode):
    def __init__(self, name, type_name):
        self.name: LexerToken = name
        self.type_name: TypeNode = type_name


class NewNode(ExpressionNode):
    def __init__(self, name):
        self.name: ExpressionCallNode = name


class DeclarationNode (ExpressionNode):
    def __init__(self, name, p_type, value):
        self.name: LexerToken = name
        self.type: TypeNode = p_type
        self.value: ExpressionNode = value


class AssignmentNode (ExpressionNode):
    def __init__(self, name: LexerToken, value: ExpressionNode):
        self.name: LexerToken = name
        self.value: ExpressionNode = value


class AssignmentPropertyNode(ExpressionNode):
    def __init__(self, name: LexerToken, p_name: LexerToken, value: ExpressionNode) -> None:
        self.name: LexerToken = name
        self.property: LexerToken = p_name
        self.value: ExpressionNode = value


class AssignmentArrayNode(ExpressionNode):
    def __init__(self, array_call: ArrayCallNode, value: ExpressionNode) -> None:
        self.array_call: ArrayCallNode = array_call
        self.value: ExpressionNode = value


class LetNode (ExpressionNode):
    def __init__(self, assignments: List[DeclarationNode], body):
        self.assignments: List[DeclarationNode] = assignments
        self.body: ExpressionNode = body


class IfNode (ExpressionNode):
    def __init__(self, condition, body, elif_clauses, else_body):
        self.condition: ExpressionNode = condition
        self.body: ExpressionNode = body
        self.elif_clauses: List[ElifNode] = elif_clauses
        self.else_body: ExpressionNode = else_body


class ElifNode(ExpressionNode):
    def __init__(self, condition, body):
        self.condition: ExpressionNode = condition
        self.body: ExpressionNode = body


class WhileNode (ExpressionNode):
    def __init__(self, condition, body):
        self.condition: ExpressionNode = condition
        self.body: ExpressionNode = body


class ForNode (ExpressionNode):
    def __init__(self, variable: LexerToken, iterable: ExpressionNode, body):
        self.variable: LexerToken = variable
        self.iterable: ExpressionNode = iterable
        self.body: ExpressionNode = body


class ExpressionBlock(ExpressionNode):
    def __init__(self, instructions: List[ASTNode]) -> None:
        self.instructions: List[ASTNode] = instructions


class BooleanOperator(Enum):
    AND = 0
    OR = 1
    NOT = 2
    EQ = 3
    NEQ = 4
    LT = 5
    GT = 6
    LTE = 7
    GTE = 8


class ArithmeticOperator(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    POW = 4


class StringOperator(Enum):
    CONCAT = 0
    SPACED_CONCAT = 1


class ConstantTypes(Enum):
    STRING = 0
    NUMBER = 1
    BOOLEAN = 2
