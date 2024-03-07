from regex.regex import Regex, RegexBuilder
from regex.regex_grammar import RegexGrammar

b = RegexBuilder()

r = b.parse('[a-c]\\.')

m=r.value.match('a.')
print(r.value.ast)
print(m.ok)

# a=[1,23,2]
# a.reverse()
# print(a)
