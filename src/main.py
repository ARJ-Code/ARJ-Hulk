from hulk_lexer.hulk_lexer import hulk_lexer

code = input()
r = hulk_lexer.run(code)

if r.ok:
    print([t.value for t in r.tokens])
else:
    print(f'Error: {r.error.msg}\nrow:{r.error.row+1} col:{r.error.col+1} ')
