from hulk_lexer.hulk_lexer import hulk_lexer

a = hulk_lexer.run('/***/')

for i in a.tokens:
    print(i.value)
