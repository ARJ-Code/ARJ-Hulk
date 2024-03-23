from .hulk_semantic_tools import *

OBJECT = Class('Object')
STRING = Class('String')
NUMBER = Class('Number')
BOOLEAN = Class('Boolean')

EQUATABLE = Protocol('Equatable')
EQUATABLE.add_method(Method('eq', BOOLEAN, [Attribute('a1', OBJECT)]))

COMPARABLE = Protocol('Comparable')
COMPARABLE.add_method(Method('comp', NUMBER, [Attribute('a1', OBJECT)]))

ITERABLE = Protocol('Iterable')
ITERABLE.add_method(Method('next', BOOLEAN, []))
ITERABLE.add_method(Method('current', OBJECT, []))
ITERABLE.add_method(Method('reset', OBJECT, []))

INDEXABLE_GET = Protocol('IndexableGet')
INDEXABLE_GET.add_method(Method('get', OBJECT, [Attribute('a1', NUMBER)]))

INDEXABLE_SET = Protocol('IndexableSet')
INDEXABLE_SET.add_method(
    Method('set', OBJECT, [Attribute('a1', NUMBER), Attribute('a2', OBJECT)]))

OBJECT.add_method(Method('toString', STRING, []))

STRING.add_attribute(Attribute('length', NUMBER))
STRING.add_method(
    Method('eq', Method('eq', BOOLEAN, [Attribute('a1', OBJECT)])))
STRING.add_method(Method('comp', NUMBER, [Attribute('a1', OBJECT)]))
STRING.add_method(Method('get', STRING, [Attribute('a1', NUMBER)]))
STRING.add_method(Method('next', BOOLEAN, []))
STRING.add_method(Method('current', STRING, []))
STRING.add_method(Method('reset', OBJECT, []))
STRING.define_inherits(OBJECT)

NUMBER.add_method(Method('eq', BOOLEAN, [Attribute('a1', OBJECT)]))
NUMBER.add_method(Method('comp', NUMBER, [Attribute('a1', OBJECT)]))
NUMBER.define_inherits(OBJECT)

BOOLEAN.add_method(Method('eq', BOOLEAN, [Attribute('a1', OBJECT)]))
BOOLEAN.add_method(Method('comp', NUMBER, [Attribute('a1', OBJECT)]))
BOOLEAN.define_inherits(OBJECT)


def vector_t(c: Class) -> Class:
    vector = Class('['+c.name+']')
    vector.add_attribute(Attribute('dimension', NUMBER))
    vector.add_attribute(Attribute('length', NUMBER))
    vector.add_attribute(Attribute('capacity', NUMBER))
    vector.add_method(Method('add', OBJECT, [Attribute('a1', c)]))
    vector.add_method(Method('remove', OBJECT, [Attribute('a1', NUMBER)]))
    vector.add_method(Method('contains', BOOLEAN, [Attribute('a1', c)]))
    vector.add_method(Method('get', c, [Attribute('a1', NUMBER)]))
    vector.add_method(
        Method('set', OBJECT, [Attribute('a1', NUMBER), Attribute('a2', c)]))
    vector.add_method(Method('next', BOOLEAN, []))
    vector.add_method(Method('current', c, []))
    vector.add_method(Method('reset', OBJECT, []))
    vector.define_inherits(OBJECT)

m_print = Method('print', OBJECT, [Attribute('a1', OBJECT)])
m_sin = Method('sin', NUMBER, [Attribute('a1', NUMBER)])
m_cos = Method('cos', NUMBER, [Attribute('a1', NUMBER)])
m_tan = Method('tan', NUMBER, [Attribute('a1', NUMBER)])
m_exp = Method('exp', NUMBER, [Attribute('a1', NUMBER)])
m_log = Method('log', NUMBER, [Attribute(
    'a1', NUMBER), Attribute('a2', NUMBER)])
m_rand = Method('rand', NUMBER, [])

defined_class = [OBJECT, STRING, NUMBER, BOOLEAN] + \
    [vector_t(c) for c in [OBJECT, STRING, NUMBER, BOOLEAN]]
defined_protocols = [EQUATABLE, COMPARABLE,
                     ITERABLE, INDEXABLE_GET, INDEXABLE_SET]
defined_methods = [m_print, m_sin, m_cos, m_tan, m_exp, m_log, m_rand]
