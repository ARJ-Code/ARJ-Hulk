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
    def __init__(self, name: str,  returnType: 'Type', arguments: List[Attribute]) -> None:
        self.name: str = name
        self.arguments: List[Attribute] = arguments
        self.returnType: 'Type' = returnType

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name and len(self.arguments) == len(__value.arguments)

    def comp(self, method: 'Method') -> bool:
        if self.returnType.comp(method.returnType) and len(self.arguments) == len(method.arguments):
            for i in range(len(self.arguments)):
                if not self.arguments[i].type.comp(method.arguments[i].type):
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
            mc = self.get_method(mp.name)
            if mc is None and self.father is not None:
                mc = self.father.get_method(mp.name)

            find = mc is not None and mc.comp(mp)
            if not find:
                return False

        return True

    def add_protocol(self, protocol: Protocol) -> None:
        self.protocols.append(protocol)

    def comp(self, value: Type) -> bool:
        for protocol in self.protocols:
            if value == protocol:
                return True

        return super().comp(value)
