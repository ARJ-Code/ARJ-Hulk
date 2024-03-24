from typing import List, Set
from abc import ABC


class Attribute:
    def __init__(self, name: str, value: 'Type') -> None:
        self.name: str = name
        self.type: Type = value

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

    def __hash__(self) -> int:
        return hash(self.name)


class Method:
    def __init__(self, name: str,  return_type: 'Type', arguments: List[Attribute]) -> None:
        self.name: str = name
        self.arguments: List[Attribute] = arguments
        self.return_type: 'Type' = return_type

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name and len(self.arguments) == len(__value.arguments)

    def comp(self, method: 'Method') -> bool:
        if self.return_type.covariant(method.return_type) and len(self.arguments) == len(method.arguments):
            for i in range(len(self.arguments)):
                if not self.arguments[i].type.contravariant(method.arguments[i].type):
                    return False
            return True

        return False

    def __hash__(self) -> int:
        return hash(self.name)


class Type(ABC):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.methods: Set[Method] = set()
        self.father: 'Type | None' = None
        self.attributes: Set[Attribute] = set()

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

    def __hash__(self) -> int:
        return hash(self.name)
    
    def covariant(self, value: 'Type') -> bool:
        return self.comp(value)
    
    def contravariant(self, value: 'Type') -> bool:
        return value.comp(self)

    def comp(self, value: 'Type') -> bool:
        if value.name == self.name:
            return True

        return self.father is not None and self.father.comp(value)

    def add_method(self, method: Method) -> bool:
        if method in self.methods:
            return False

        m = self.get_method(method.name)
        if m is not None and not method.comp(m):
            return False

        self.methods.add(method)
        return True

    def add_attribute(self, attribute: Attribute) -> bool:
        if attribute in self.attributes:
            return False

        a = self.get_attribute(attribute.name)
        if a is not None and not attribute.comp(a):
            return False

        self.attributes.add(attribute)
        return True

    def get_method(self, name: str) -> Method | None:
        for method in self.methods:
            if method.name == name:
                return method
        if self.father is not None:
            return self.father.get_method(name)
        return None

    def get_attribute(self, name: str) -> Attribute | None:
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute
        if self.father is not None:
            return self.father.get_attribute(name)
        return None


class Protocol(Type):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def define_extends(self, extends: 'Protocol') -> None:
        self.father = extends


class Class(Type):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.protocols: List[Protocol] = []

    def define_inherits(self, inherits: 'Class') -> None:
        self.father = inherits

    def implement_protocol(self, protocol: Protocol) -> bool:
        for mp in protocol.methods:
            m = self.get_method(mp.name)
            if m is None or not m.comp(mp):
                return False
        return True

    def add_protocol(self, protocol: Protocol) -> None:
        self.protocols.append(protocol)

    def comp(self, value: Type) -> bool:
        for protocol in self.protocols:
            if value == protocol:
                return True

        return super().comp(value)

class Scope:
    def __init__(self, parent=None) -> None:
        self.parent: Scope = parent
        self.attributes: List[Attribute] = []
        self.methods: Set[Method] = set()
        self.classes: Set[Class] = set()
        self.protocols: Set[Protocol] = set()
        self.attribute_index = 0 if parent is None else len(parent.attributes)

    def define_attribute(self, attribute: Attribute) -> bool:
        a = self.get_defined_attribute(attribute.name, len(self.attributes))
        if a is not None:
            return False
        
        self.attributes.append(attribute)
        return True

    def define_method(self, method: Method) -> bool:
        m = self.get_defined_method(method.name)
        if m is not None and not m.comp(method):
            return False
        
        self.methods.add(method)
        return True
    
    def define_class(self, class_: Class) -> bool:
        c = self.get_defined_type(class_.name)
        if c is not None and not c.comp(class_):
            return False
        
        self.classes.add(class_)
        return True
    
    def define_protocol(self, protocol: Protocol) -> bool:
        p = self.get_defined_type(protocol.name)
        if p is not None and not p.comp(protocol):
            return False
        
        self.protocols.add(protocol)
        return True
    
    def get_defined_attribute(self, name: str, index: int) -> Attribute | None:
        for i in range(index):
            attribute: Attribute = self.attributes[i].name
            if attribute.name == name:
                return attribute
        if self.parent is not None:
            return self.parent.get_defined_attribute(name, self.attribute_index)
        return None

    def get_defined_method(self, name: str) -> Method | None:
        for method in self.methods:
            if method.name == name:
                return method
        if self.parent is not None:
            return self.parent.get_defined_method(name)
        return None

    def get_defined_type(self, name: str) -> Type | None:
        for class_ in self.classes:
            if class_.name == name:
                return class_
        for protocol in self.protocols:
            if protocol.name == name:
                return protocol
        if self.parent is not None:
            return self.parent.get_defined_type(name)
        return None