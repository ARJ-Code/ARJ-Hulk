from abc import ABC
from enum import Enum
from typing import List


class ASTNode (ABC):
    pass

class InstructionNode (ASTNode):
    pass

class ExpressionNode (ASTNode):
    pass

class BinaryNode (ExpressionNode):
    def __init__(self, left, right):
        self.left: ASTNode = left
        self.right: ASTNode = right

class UnaryNode (ExpressionNode):
    def __init__(self, child):
        self.child: ASTNode = child        

class AtomicNode(ExpressionNode):
    def __init__(self, name):
        self.name: str = name

class ListNode(ASTNode):
    def __init__(self, left, right):
        self.left: ListNode = left
        self.right: ASTNode = right

class ConstantNode (AtomicNode):
    def __init__(self, value, type):
        super().__init__(value)
        self.value = value
        self.type: ConstantTypes = type        

class TypeNode (ASTNode):
    def __init__(self, name):
        self.name: str = name     

class LetExpressionNode (BinaryNode):
    def __init__(self, assignments, body):
        super().__init__(assignments, body)    

class LetInstructionNode (InstructionNode):
    def __init__(self, assignments):
        self.assignments: List[AssignmentNode] = assignments            


class AritmeticBinaryNode (BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator: AritmeticOperator = operator    

class AritmeticUnaryNode (UnaryNode):
    def __init__(self, child, operator):
        super().__init__(child)
        self.operator: AritmeticOperator = operator

class BooleanBinaryNode (BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator: BooleanOperator = operator

class BooleanUnaryNode (UnaryNode):
    def __init__(self, child, operator):
        super().__init__(child)
        self.operator: BooleanOperator = operator

class FunctionDeclarationNode (InstructionNode):
    def __init__(self, name, parameters, body, return_type):
        self.name: str = name
        self.parameters: List[str] = parameters
        self.body: ASTNode = body
        self.return_type: str = return_type                

class FunctionCallNode (AtomicNode):
    def __init__(self, name, parameters):
        super().__init__(name, AtomicTypes.CALL)
        self.parameters: List[ExpressionNode] = parameters


class StringExpressionNode (BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator: StringOperator = operator

class AssignmentExpressionNode (BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)

class AssignmentInstructionNode (InstructionNode):
    def __init__(self, name, type, value):
        self.name: str = name
        self.type: TypeNode = type
        self.value: ExpressionNode = value

class IfNode (ASTNode):
    def __init__(self, condition, then_body, else_body):
        self.condition: BooleanBinaryNode | BooleanUnaryNode = condition
        self.then_body: ASTNode = then_body

class WhileNode (ASTNode):
    def __init__(self, condition, body):
        self.condition: BooleanExpressionNode = condition
        self.body: ASTNode = body        

class ForNode (ASTNode):
    def __init__(self, name, start, end, body):
        self.name: str = name
        self.start: ExpressionNode = start
        self.end: ExpressionNode = end
        self.body: ASTNode = body

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

class AritmeticOperator(Enum):
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
    VOID = 3


    