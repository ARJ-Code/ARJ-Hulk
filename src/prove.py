import re

a=re.compile('/\/\*[\s\S]*?\*\//')

print(a.match('/*aaa*/'))