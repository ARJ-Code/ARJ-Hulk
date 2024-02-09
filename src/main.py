from hulk_lexer.analyzer import DigitAnalyzer, PatternAnalyzer, ManyAnalyzer, PatternAnalyzer, AlphaNumericAnalyzer, AndAnalyzer, OrAnalyzer, ConditionalAnalyzer, or_patterns


print(or_patterns('e', 'e+').analyzers[0].match(0, 'e'))
a = ManyAnalyzer(DigitAnalyzer())
b = ConditionalAnalyzer(or_patterns('e', 'e+'), a)
c = AndAnalyzer(a, b)

s = "233e+33"

r = c.run(0, 0, 0, s)

print(r.token)
