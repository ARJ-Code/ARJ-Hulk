from lexer.analyzer import NumberAnalyzer

a=NumberAnalyzer()

s='1e2.39'

print(a.analyze(s,0,0,0).ok)