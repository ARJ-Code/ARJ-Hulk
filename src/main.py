from hulk_parser.analyzer import NumberAnalyzer,StringAnalyzer,SpaceAnalyzer
from hulk_parser.lexer import lexer
a=StringAnalyzer()

s='\"1e2.\\nooo39\" 122    122'

# print(a.analyze(s,0,0,0).ok)

q=1e3

print(lexer(s,[NumberAnalyzer(),StringAnalyzer(),SpaceAnalyzer()]))

print(float('1e-1'))