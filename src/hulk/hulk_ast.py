from abc import ABC
from enum import Enum
from typing import List


class ASTNode (ABC):
    pass

class ExpressionNode (ASTNode):
    def __init__(self, type):
        self.type: str = type

class BinaryNode (ASTNode):
    def __init__(self, left, right):
        self.left: ASTNode = left
        self.right: ASTNode = right

class AritmeticExpressionNode (BinaryNode, ExpressionNode):
    def __init__(self, left, right, operator, type):
        super().__init__(left, right, type)
        self.operator: AritmeticOperator = operator    

class BooleanExpressionNode (BinaryNode, ExpressionNode):
    def __init__(self, left, right, operator, type):
        super().__init__(left, right, type)
        self.operator: BooleanOperator = operator

class FunctionNode (ASTNode):
    def __init__(self, name, parameters, body, return_type):
        self.name: str = name
        self.parameters: List[str] = parameters
        self.body: ASTNode = body
        self.return_type: str = return_type                

class FunctionCallNode (ASTNode):
    def __init__(self, name, parameters):
        self.name: str = name
        self.parameters: List[str] = parameters

class StringExpressionNode (BinaryNode, ExpressionNode):
    def __init__(self, left, right, operator, type):
        super().__init__(left, right, type)
        self.operator: StringOperator = operator


class LetNode (ASTNode):
    def __init__(self, name, value, type):
        self.name: str = name
        self.value: ExpressionNode = value
        self.type: str = type

class AssignmentNode (ASTNode):
    def __init__(self, name, value):
        self.name: str = name
        self.value: ExpressionNode = value

class IfNode (ASTNode):
    def __init__(self, condition, then_body, else_body):
        self.condition: BooleanExpressionNode = condition
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

class AritmeticOperator(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    POW = 4    

class StringOperator(Enum):
    CONCAT = 0
    SPACEDCONCAT = 1    



    