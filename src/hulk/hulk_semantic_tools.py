from typing import List, Set, Tuple, Dict

from compiler_tools.lexer import LexerToken
from hulk.hulk_defined import *
from collections import OrderedDict
from typing import List, Set, Tuple, Dict
from abc import ABC
from compiler_tools.lexer import LexerToken


class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]


class Attribute:
    def __init__(self, name: str, value: 'Type') -> None:
        self.name: str = name
        self.type: Type = value

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        output = f'{self.name}' + (f' : {self.type.name}' if self.type else '')
        return output


class Method:
    def __init__(self, name: str, return_type: 'Type', arguments: List[Attribute] = []) -> None:
        self.name: str = name
        self.arguments: List[Attribute] = arguments
        self.return_type: 'Type' = return_type

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name and len(self.arguments) == len(__value.arguments)

    def __hash__(self) -> int:
        return hash(self.name)

    def comp(self, value: 'Method') -> bool:
        if self.name != value.name or len(self.arguments) != len(value.arguments):
            return False

        for i in range(len(self.arguments)):
            if self.arguments[i].type != value.arguments[i].type:
                return False

        return True

    def is_overriding(self, value: 'Method'):
        if self.name != value.name or len(self.arguments) != len(value.arguments):
            return False

        for i in range(len(self.arguments)):
            if self.arguments[i].type != value.arguments[i].type:
                return False

        if self.return_type != value.return_type:
            return False

        return True

    def __str__(self) -> str:
        output = f'{self.name}('
        output += ', '.join(str(x) for x in self.arguments)
        output += f') -> {self.return_type.name}' if self.return_type else ')'
        return output


class Type(ABC):
    def __init__(self, name: str):
        self.name = name
        self.attributes: List[Attribute] = []
        self.methods: List[Method] = []
        self.protocols: List[Protocol] = []
        self.parent: Type = None

    def decompact(self, token: LexerToken):
        return (token.row, token.col, token.value)

    def error_location(self, row, col) -> str:
        return f' Error at {row}:{col}'

    def set_parent(self, parent: 'Type') -> None:
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, id: LexerToken) -> Attribute:
        row, col, name = self.decompact(id)
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(
                    f'Attribute "{name}" is not defined in {self.name}.' + self.error_location(row, col))
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(
                    f'Attribute "{name}" is not defined in {self.name}.' + self.error_location(row, col))

    def define_attribute(self, id: LexerToken, typex: 'Type') -> Attribute:
        row, col, name = self.decompact(id)
        if name in (attribute.name for attribute in self.attributes):
            raise SemanticError(
                f'Attribute "{name}" already defined in {self.name}' + self.error_location(row, col))

        attribute = Attribute(name, typex)
        self.attributes.append(attribute)
        return attribute

    def add_attribute(self, attribute: Attribute):
        self.attributes.append(attribute)

    def get_method(self, name: str) -> Method:
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(
                    f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(
                    f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, id: LexerToken, arguments: List[Attribute], return_type: 'Type') -> Method:
        row, col, name = self.decompact(id)
        if name in (method.name for method in self.methods):
            raise SemanticError(
                f'Method "{name}" already defined in {self.name}' + self.error_location(row, col))

        method = Method(name, return_type, arguments)
        self.methods.append(method)
        return method

    def add_method(self, method: Method):
        self.methods.append(method)

    def all_attributes(self, clean=True) -> List[Tuple[Attribute, 'Type']]:
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True) -> List[Tuple[Method, 'Type']]:
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other: 'Type') -> bool:
        if self == other:
            return True
        if self.parent is not None:
            return self.parent.conforms_to(other)
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

    def __hash__(self) -> int:
        return hash(self.name)


class Protocol(Type):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def set_parent(self, parent: Type) -> None:
        return self.define_extends(parent)

    def define_extends(self, extends: 'Protocol') -> None:
        self.parent = extends

    def __str__(self):
        output = f'protocol {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.methods else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output


class Class(Type):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.protocols: List[Protocol] = []
        self.params: List[Attribute] = []
        # for param in params:
        #     self.add_attribute(param)

    def set_parent(self, parent: Type) -> None:
        return self.define_inherits(parent)

    def add_param(self, param: Attribute) -> None:
        self.params.append(param)

    def define_inherits(self, inherits: 'Class') -> None:
        self.parent = inherits

    def implement_protocol(self, protocol: Protocol) -> bool:
        for mp in protocol.methods:
            finded = False
            class_methods = self.all_methods()
            for mc in class_methods:
                if mc.name == mp.name and len(mc.arguments) == len(mp.arguments):
                    if mc.return_type.conforms_to(mp.return_type):
                        if all([ap.type.conforms_to(ac.type) for ap, ac in zip(mp.arguments, mc.arguments)]):
                            finded = True
                            break
            if not finded:
                return False
        return True

    def add_protocol(self, protocol: Protocol) -> None:
        self.protocols.append(protocol)

    # def add_parents_methods(self):
    #     parents_methods = self.parent.all_methods()
    #     for m1 in parents_methods:
    #         are_override = False
    #         for m2 in self.methods:
    #             if m2.is_overriding(m1):
    #                 are_override = True

    def __str__(self):
        output = f'type {self.name}'
        output += f'({", ".join(str(x) for x in self.params)})' if self.params else ''
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods or self.protocols else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '\n\t'.join(str(x) for x in self.protocols)
        output += '\n' if self.protocols else ''
        output += '}\n'
        return output


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

    def check_valid_params(self, id: LexerToken, parameters) -> Function:
        row, col, name = self.decompact(id)
        function_ = self.get_defined_function(id)
        if len(function_.args) != len(parameters):
            raise SemanticError(
                f'Invalid amount of arguments while calling function {name}.' + self.error_location(row, col))
        return function_
    
    def get_defined_type(self, id: LexerToken) -> TypeSemantic:
        row, col, name = self.decompact(id)
        for t in self.types:
            if t.name == name:
                return t
        if self.parent is not None:
            return self.parent.get_defined_type(id)
        raise SemanticError(
            f'Type {name} is not defined.' + self.error_location(row, col))


class SemanticResult:
    def __init__(self, context: Context, errors: List[str]) -> None:
        self.ok = len(errors) == 0
        self.context = context
        self.errors = errors
   