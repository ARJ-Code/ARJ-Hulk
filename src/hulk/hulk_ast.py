from abc import ABC
from enum import Enum
from typing import List

# level 0
class ASTNode (ABC):
    pass


# level 1
class InstructionNode (ASTNode):
    pass

class ExpressionNode (ASTNode):
    pass

class ListNode(ASTNode):
    def __init__(self, left, right):
        self.left: ListNode = left
        self.right: ASTNode = right

class TypeNode (ASTNode):
    def __init__(self, name):
        self.name: str = name    

class EOFNode (ASTNode):
    pass 


# level 2
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




class FunctionCallNode (AtomicNode):
    def __init__(self, name, parameters):
        super().__init__(name)
        self.parameters: ListNode = parameters

class AttributedNode(AtomicNode):
    def __init__(self, base_instance, property_access):
        self.base_instance = base_instance  
        self.property_access = property_access 

class ConstantNode (AtomicNode):
    def __init__(self, value, type):
        super().__init__(value)
        self.value = value
        self.type: ConstantTypes = type     


class StringBinaryNode (BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator: StringOperator = operator       

class AritmethicBinaryNode (BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator: AritmethicOperator = operator    

class AritmethicUnaryNode (UnaryNode):
    def __init__(self, child, operator):
        super().__init__(child)
        self.operator: AritmethicOperator = operator


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
        self.parameters = parameters
        self.body: ExpressionNode = body
        self.return_type: str = return_type                










class DeclarationNode (ExpressionNode):
    def __init__(self, name, type, value):
        self.name: str = name
        self.type: TypeNode = type
        self.value: ExpressionNode = value

class AssignmentNode (ExpressionNode):
    def __init__(self, name, value):
        self.name: str = name
        self.value: ExpressionNode = value

class LetNode(ExpressionNode):
    def __init__(self, assignments):
        self.assignments: ListNode = assignments


class LetBodyNode (LetNode):
    def __init__(self, assignments, body):
        super().__init__(assignments)    
        self.body: ExpressionNode = body


class IfNode (ExpressionNode):
    def __init__(self, condition, body, elif_clauses, else_body):
        self.condition: ExpressionNode = condition
        self.body: ExpressionNode = body
        self.elif_clauses: ExpressionNode | EOFNode = elif_clauses
        self.else_body: ExpressionNode | EOFNode = else_body

class WhileNode (ExpressionNode):
    def __init__(self, condition, body):
        self.condition: ExpressionNode = condition
        self.body: ExpressionNode = body        

class ForNode (ExpressionNode):
    def __init__(self, variable, iterable, body):
        self.variable: str = variable
        self.iterable: ExpressionNode = iterable
        self.body: ExpressionNode = body

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

class AritmethicOperator(Enum):
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


    