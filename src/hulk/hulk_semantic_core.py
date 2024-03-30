from abc import ABC
from collections import OrderedDict
from typing import List, Tuple

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
                return self.parent.get_attribute(id)
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

    @staticmethod
    def low_common_ancester(t1: 'Type', t2: 'Type') -> 'Type':
        ERROR = Type('Error')
        if t1 is None and t2 is None:
            return ERROR
        elif t1 is None:
            return t2
        elif t2 is None:
            return t1
        elif t1 == ERROR or t2 == ERROR:
            return ERROR
        elif t1.conforms_to(t2):
            return t2
        elif t2.conforms_to(t1):
            return t1
        else:
            return Type.low_common_ancester(t1.parent, t2.parent)

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
            for mc, _ in class_methods:
                if mc.name == mp.name and len(mc.arguments) == len(mp.arguments):
                    if mc.return_type is None or any([a for a in mc.arguments if a.type is None]):
                        continue
                    if mc.return_type.conforms_to(mp.return_type):
                        if all([ap.type.conforms_to(ac.type) for ap, ac in zip(mp.arguments, mc.arguments)]):
                            finded = True
                            break
            if not finded:
                return False
        return True

    def add_protocol(self, protocol: Protocol) -> None:
        self.protocols.append(protocol)

    def conforms_to(self, other: 'Type') -> bool:
        if other in self.protocols:
            return True

        return super().conforms_to(other)

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
