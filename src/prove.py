from regex.regex_lexer import lexer

l = lexer('$\$e[34]\$').value

for i in l:
    print(i)

print(l[1].is_special)
