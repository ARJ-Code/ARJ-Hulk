from hulk.hulk_lexer import hulk_lexer_load
from hulk.hulk_constants import *


def test():
    hulk_lexer = hulk_lexer_load()
    l1 = hulk_lexer.run('a+we+_we')
    assert l1.ok
    assert l1.tokens[0].value == 'a'
    assert l1.tokens[0].type == IDENTIFIER

    l2 = hulk_lexer.run('foreach { }')
    assert len(l2.tokens) == 3
    assert l2.tokens[0].type == IDENTIFIER

    l3 = hulk_lexer.run('//kadjnvjnd\n')
    assert len(l3.tokens) == 0

    l4 = hulk_lexer.run('099')
    assert len(l4.tokens) == 2

    l5 = hulk_lexer.run('wee\n"\q"')
    assert not l5.ok
    assert l5.error.col == 0
    assert l5.error.row == 1

    l6 = hulk_lexer.run('@@+/|')
    assert len(l6.tokens) == 4
