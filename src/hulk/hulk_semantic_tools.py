from collections import OrderedDict
from typing import List, Set
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
        output = f'{self.name}' + (': Error' if self.type is None else f': {self.type.name}')
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
    
    def __str__(self) -> str:
        output = f'method {self.name}('
        output += ', '.join(str(x) for x in self.arguments)
        output += ') -> Error' if self.return_type is None else f') -> {self.return_type.name}'
        return output

class Type(ABC):
    def __init__(self, name:str):
        self.name = name
        self.attributes: List[Attribute] = []
        self.methods: List[Method] = []
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
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.' + self.error_location(row, col))
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.' + self.error_location(row, col))

    def define_attribute(self, id: LexerToken, typex: 'Type') -> Attribute:
        row, col, name = self.decompact(id)
        if name in (attribute for attribute in self.all_attributes()):
            raise SemanticError(f'Attribute "{name}" already defined in {self.name}' + self.error_location(row, col))

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
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, id: LexerToken, arguments: List[Attribute], return_type: 'Type') -> Method:
        row, col, name = self.decompact(id)
        if name in (method for method in self.all_methods()):
            raise SemanticError(f'Method "{name}" already defined in {self.name}' + self.error_location(row, col))

        method = Method(name, return_type, arguments)
        self.methods.append(method)
        return method
    
    def add_method(self, method: Method):
        self.methods.append(method)

    def all_attributes(self, clean=True) -> List[Attribute]:
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True) -> List[Method]:
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

# class Type(ABC):
#     def __init__(self, name: str) -> None:
#         self.name: str = name
#         self.methods: Set[Method] = set()
#         self.father: 'Type | None' = None
#         self.attributes: Set[Attribute] = set()

#     def __eq__(self, __value: object) -> bool:
#         return self.name == __value.name

#     def __hash__(self) -> int:
#         return hash(self.name)
    
#     def covariant(self, value: 'Type') -> bool:
#         return self.comp(value)
    
#     def contravariant(self, value: 'Type') -> bool:
#         return value.comp(self)

#     def comp(self, value: 'Type') -> bool:
#         if value.name == self.name:
#             return True

#         return self.father is not None and self.father.comp(value)

#     def add_method(self, method: Method) -> bool:
#         if method in self.methods:
#             return False

#         m = self.get_method(method.name)
#         if m is not None and not method.comp(m):
#             return False

#         self.methods.add(method)
#         return True

#     def add_attribute(self, attribute: Attribute) -> bool:
#         if attribute in self.attributes:
#             return False

#         a = self.get_attribute(attribute.name)
#         if a is not None and not attribute.comp(a):
#             return False

#         self.attributes.add(attribute)
#         return True

#     def get_method(self, name: str) -> Method | None:
#         for method in self.methods:
#             if method.name == name:
#                 return method
#         if self.father is not None:
#             return self.father.get_method(name)
#         return None

#     def get_attribute(self, name: str) -> Attribute | None:
#         for attribute in self.attributes:
#             if attribute.name == name:
#                 return attribute
#         if self.father is not None:
#             return self.father.get_attribute(name)
#         return None


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
    def __init__(self, name: str, params: List[Attribute] = []) -> None:
        super().__init__(name)
        self.protocols: List[Protocol] = []
        self.params = params
        for param in params:
            self.add_attribute(param)

    def set_parent(self, parent: Type) -> None:
        return self.define_inherits(parent)

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
    
    def __str__(self):
        output = f'type {self.name}'
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
        self.types: {str, Type} = {}
        self.protocols: {str, Type} = {}

    def decompact(self, token: LexerToken):
        return (token.row, token.col, token.value)
    
    def error_location(self, row, col) -> str:
        return f' Error at {row}:{col}'

    def create_type(self, id: LexerToken) -> Class:
        row, col, name = self.decompact(id)
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.' + self.error_location(row, col))
        typex = self.types[name] = Class(name)
        return typex
    
    def create_protocol(self, id: LexerToken) -> Protocol:
        row, col, name = self.decompact(id)
        if name in self.protocols:
            raise SemanticError(f'Protocol with the same name ({name}) already in context.' + self.error_location(row, col))
        protocol = self.protocols[name] = Protocol(name)
        return protocol
    
    def add_type(self, type: Class) -> Class:
        typex = self.types[type.name] = type
        return typex
    
    def add_protocol(self, protocol: Protocol) -> Protocol:
        self.protocols[protocol.name] = protocol
        return protocol

    def get_type(self, id: LexerToken) -> Class:
        row, col, name = self.decompact(id)
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.'+ self.error_location(row, col))
        
    def get_protocol(self, id: LexerToken) -> Protocol:
        row, col, name = self.decompact(id)
        try:
            return self.protocols[name]
        except KeyError:
            raise SemanticError(f'Protocol "{name}" is not defined.'+ self.error_location(row, col))

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n\t' + \
            '\n\t'.join(y for x in self.protocols.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

# class Scope:
#     def __init__(self, parent=None) -> None:
#         self.parent: Scope = parent
#         self.attributes: List[Attribute] = []
#         self.methods: Set[Method] = set()
#         self.classes: Set[Class] = set()
#         self.protocols: Set[Protocol] = set()
#         self.attribute_index = 0 if parent is None else len(parent.attributes)

#     def create_child_scope(self) -> 'Scope':
#         return Scope(self)

#     def define_attribute(self, attribute: Attribute) -> bool:
#         a = self.get_defined_attribute(attribute.name, len(self.attributes))
#         if a is not None:
#             return False
        
#         self.attributes.append(attribute)
#         return True

#     def define_method(self, method: Method) -> bool:
#         m = self.get_defined_method(method.name)
#         if m is not None and not m.comp(method):
#             return False
        
#         self.methods.add(method)
#         return True
    
#     def define_class(self, class_: Class) -> bool:
#         c = self.get_defined_type(class_.name)
#         if c is not None and not c.comp(class_):
#             return False
        
#         self.classes.add(class_)
#         return True
    
#     def define_protocol(self, protocol: Protocol) -> bool:
#         p = self.get_defined_type(protocol.name)
#         if p is not None and not p.comp(protocol):
#             return False
        
#         self.protocols.add(protocol)
#         return True
    
#     def get_defined_attribute(self, name: str, index: int) -> Attribute | None:
#         for i in range(index):
#             attribute: Attribute = self.attributes[i].name
#             if attribute.name == name:
#                 return attribute
#         if self.parent is not None:
#             return self.parent.get_defined_attribute(name, self.attribute_index)
#         return None

#     def get_defined_method(self, name: str) -> Method | None:
#         for method in self.methods:
#             if method.name == name:
#                 return method
#         if self.parent is not None:
#             return self.parent.get_defined_method(name)
#         return None

#     def get_defined_type(self, name: str) -> Type | None:
#         for class_ in self.classes:
#             if class_.name == name:
#                 return class_
#         for protocol in self.protocols:
#             if protocol.name == name:
#                 return protocol
#         if self.parent is not None:
#             return self.parent.get_defined_type(name)
#         return None