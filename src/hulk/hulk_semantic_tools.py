from typing import List, Set, Tuple, Dict

from compiler_tools.lexer import LexerToken
from hulk.hulk_defined import *


class Context:
    def __init__(self):
        self.types: Dict[str, Type] = {}
        self.protocols: Dict[str, Type] = {}
        self.methods: Dict[str, Method] = {}

    def decompact(self, token: LexerToken):
        return (token.row, token.col, token.value)

    def error_location(self, row, col) -> str:
        return f' Error at {row}:{col}'

    def create_type(self, id: LexerToken) -> Class:
        row, col, name = self.decompact(id)
        if name in self.types:
            raise SemanticError(
                f'Type with the same name ({name}) already in context.' + self.error_location(row, col))
        typex = self.types[name] = Class(name)
        return typex

    def create_protocol(self, id: LexerToken) -> Protocol:
        row, col, name = self.decompact(id)
        if name in self.protocols:
            raise SemanticError(
                f'Protocol with the same name ({name}) already in context.' + self.error_location(row, col))
        protocol = self.protocols[name] = Protocol(name)
        return protocol

    def create_method(self, id: LexerToken, parameters: List[Attribute], return_type: Type) -> Method:
        row, col, name = self.decompact(id)
        if name in self.methods:
            raise SemanticError(
                f'Method with the same name ({name}) already in context.' + self.error_location(row, col))
        method = self.methods[name] = Method(name, return_type, parameters)
        return method

    def add_type(self, type: Class) -> Class:
        typex = self.types[type.name] = type
        return typex

    def add_protocol(self, protocol: Protocol) -> Protocol:
        self.protocols[protocol.name] = protocol
        return protocol

    def add_method(self, method: Method) -> Method:
        self.methods[method.name] = method
        return method

    def get_type(self, id: LexerToken) -> Class:
        row, col, name = self.decompact(id)
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(
                f'Type "{name}" is not defined.' + self.error_location(row, col))

    def get_protocol(self, id: LexerToken) -> Protocol:
        row, col, name = self.decompact(id)
        try:
            return self.protocols[name]
        except KeyError:
            raise SemanticError(
                f'Protocol "{name}" is not defined.' + self.error_location(row, col))

    def get_method(self, id: LexerToken) -> Method:
        row, col, name = self.decompact(id)
        try:
            return self.methods[name]
        except KeyError:
            raise SemanticError(
                f'Protocol "{name}" is not defined.' + self.error_location(row, col))

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n\t' + \
            '\n\t'.join(y for x in self.protocols.values()
                        for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)


class SemanticGraph:
    def __init__(self):
        self.adj: List[List[int]] = []
        self.nodes: List[SemanticNode] = []
        self.index: int = 0
        self.ERROR = Type('Error')
        self.VECTOR = Type('Vector')

    def add_node(self, node_type: Type = None) -> 'SemanticNode':
        new_node = SemanticNode(self.index, node_type)
        self.index = self.index + 1
        self.nodes.append(new_node)
        self.adj.append([])
        return new_node

    def add_path(self, parent: 'SemanticNode', child: 'SemanticNode') -> 'SemanticNode':
        self.adj[parent.index].append(child.index)
        return parent

    def get_children(self, node: 'SemanticNode') -> List['SemanticNode']:
        return [self.nodes[i] for i in self.adj[node.index]]

    def dfs(self, node: 'SemanticNode') -> Type:
        if len(self.get_children(node)) == 0:
            node.node_type = self.ERROR if node.node_type is None else node.node_type
            if node.node_type == self.VECTOR:
                node.node_type = vector_t(OBJECT, 1)
            node.visited = True
            return node.node_type
        children_type = None
        for child in self.get_children(node):
            if not child.visited:
                self.dfs(child)
            children_type = Type.low_common_ancester(
                children_type, child.node_type)
        if node.node_type is None:
            node.node_type = children_type
        elif node.node_type == self.VECTOR:
            node.node_type = vector_t(children_type, 1)
        elif not children_type.conforms_to(node.node_type):
            node.node_type = self.ERROR
        node.visited = True
        return node.node_type

    def type_inference(self) -> bool:
        nodes = self.nodes
        nodes.sort(key=lambda n: n.index)
        for node in nodes:
            if not node.visited:
                if self.dfs(node) == self.ERROR:
                    raise SemanticError(f'Incorrect type declaration')

    def g_transp(self):
        new_ajd = [[] for _ in range(len(self.adj))]
        for i in range(self.adj):
            for j in self.adj[i]:
                new_ajd[j].append(i)
        return new_ajd

    def dfs_visit(self, n: int, adj: List[List[int]], mask: List[bool], q: List[int], cc: int, cc_list: List[int]):
        mask[n] = True

        for i in adj[n]:
            if not mask[i]:
                self.dfs_visit(i, adj, mask, q, cc, cc_list)

        if cc == -1:
            q.append(n)
        else:
            cc_list[n] = cc

    def tarjans(self) -> List[int]:
        new_adj = self.g_transp()

        mask = [False for _ in range(len(self.adj))]
        cc_list = [-1 for _ in range(len(self.adj))]

        q = []

        for i in range(len(self.adj)):
            if mask[i]:
                continue

            self.dfs_visit(i, self.adj, mask, q, -1, cc_list)

        mask = [False for _ in range(len(self.adj))]

        ind = 0

        while len(q) != 0:
            act = q[-1]
            q.pop()

            if not mask[act]:

                self.dfs_visit(act, new_adj, mask, q, ind, cc_list)
                ind += 1

        return cc_list


class SemanticNode(object):
    def __init__(self, index: int, node_type: Type = None):
        self.index = index
        self.node_type = node_type
        self.visited: bool = False


class Variable:
    def __init__(self, name: str, node: SemanticNode) -> None:
        self.name: str = name
        self.node: SemanticNode = node


class Function:
    def __init__(self, name: str, node: SemanticNode, args: List[SemanticNode]) -> None:
        self.name = name
        self.node = node
        self.args = args

    def check_valid_params(self, id: LexerToken, parameters) -> 'Function':
        row, col, name = (id.row, id.col, id.value)
        if len(self.args) != len(parameters):
            raise SemanticError(
                f'Invalid amount of arguments while calling function {name}.' + f' Error at {row}:{col}')
        return self


class TypeSemantic:
    def __init__(self, name: str, functions: List[Function], attributes: List[Variable]) -> None:
        self.name: str = name
        self.functions: List[Function] = functions
        self.attributes: List[Variable] = attributes

    def get_function(self, name: str) -> Function | None:
        for f in self.functions:
            if name == f.name:
                return f
        return None

    def get_attribute(self, name: str) ->Variable | None:
        for a in self.attributes:
            if name == a.name:
                return a
        return None


class Scope:
    def __init__(self, parent: 'Scope' = None) -> None:
        self.parent: Scope = parent
        self.variables: List[Variable] = []
        self.functions: List[Function] = []
        self.types: List[TypeSemantic] = []
        # self.variables: {str, SemanticNode} = {}
        # self.attributes: List[Attribute] = []
        # self.methods: Set[Method] = set()
        # self.attribute_index = 0 if parent is None else len(parent.attributes)

    def decompact(self, token: LexerToken):
        return (token.row, token.col, token.value)

    def error_location(self, row, col) -> str:
        return f' Error at {row}:{col}'

    def create_child_scope(self) -> 'Scope':
        return Scope(self)

    def define_variable(self, id: LexerToken, node: SemanticNode) -> SemanticNode:
        row, col, name = self.decompact(id)
        self.variables.append(Variable(name, node))
        return node

    def get_defined_variable(self, id: LexerToken) -> Variable:
        row, col, name = self.decompact(id)
        for variable in self.variables:
            if variable.name == name:
                return variable
        if self.parent is not None:
            return self.parent.get_defined_variable(id)
        raise SemanticError(
            f'Variable {name} is not defined.' + self.error_location(row, col))

    def define_function(self, name: str, node: SemanticNode, args: List[SemanticNode]) -> SemanticNode:
        self.functions.append(Function(name, node, args))
        return node

    def define_type(self, name: str, functions: List[Function], attributes: List[Variable]):
        self.types.append(TypeSemantic(name, functions, attributes))

    def get_defined_function(self, id: LexerToken) -> Function:
        row, col, name = self.decompact(id)
        for function_ in self.functions:
            if function_.name == name:
                return function_
        if self.parent is not None:
            return self.parent.get_defined_function(id)
        raise SemanticError(
            f'Function {name} is not defined.' + self.error_location(row, col))

    def get_defined_type(self, id: LexerToken) -> TypeSemantic:
        row, col, name = self.decompact(id)
        for t in self.types:
            if t.name == name:
                return t
        if self.parent is not None:
            return self.parent.get_defined_type(id)
        raise SemanticError(
            f'Type {name} is not defined.' + self.error_location(row, col))
