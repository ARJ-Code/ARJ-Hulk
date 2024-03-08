from regex.regex import Regex, RegexBuilder
from regex.regex_grammar import RegexGrammar

b = RegexBuilder()
# b.build()

r = b.parse('"(\\\\[\\\\trn"]|[^"])*"')

m=r.value.match('"ass\\\"s"')

print(m.value)

# a=[1,23,2]
# a.reverse()
# print(a)
