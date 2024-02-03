from parser.analyzer import NumberAnalyzer,StringAnalyzer

a=StringAnalyzer()

s='\"1e2.\\nooo39\"'

# print(a.analyze(s,0,0,0).ok)

print(a.run(s,0,0,0).token.value)