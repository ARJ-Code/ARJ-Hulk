from hulk_lexer.hulk_lexer import hulk_lexer, ignore_analyzer,string_analyzer

l = hulk_lexer.run('a2222a2+2')

# s=string_analyzer.run("\"\\n")
# print()
print([t.value for t in l.tokens])

# q = ignore_analyzer.run(0, 0, 0, "//errr\n")
# print(q.ok)
# print(ignore_analyzer.match(0,"   /* errr */"))
