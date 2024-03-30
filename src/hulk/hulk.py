from hulk.hulk_semantic_check import hulk_semantic_check
from .hulk_lexer import hulk_lexer_build
from .hulk_parser import hulk_parser_build, hulk_to_grammar, hulk_parse
from compiler_tools.lexer import Lexer
from .hulk_grammar import hulk_grammar
from .hulk_code_generator import hulk_code_generator
import subprocess


def hulk_build() -> bool:
    hulk_lexer_build()
    return hulk_parser_build()


def hulk_compile_str(program: str) -> bool:
    hulk_lexer = Lexer()
    hulk_lexer.load('hulk')

    result = hulk_lexer.run(program)
    tokens = result.tokens

    if not result.ok:
        print(
            f'Lexer error:\nrow {result.error.row+1} col {result.error.col+1}')
        return False

    result = hulk_parse([hulk_to_grammar(t) for t in result.tokens])

    if not result.ok:
        print(
            f'Parser error:\nrow {tokens[result.error-1].row+1} col {tokens[result.error-1].col+1}')
        return False

    ast = hulk_grammar.evaluate(result.derivation_tree, tokens)
    result = hulk_semantic_check(ast)

    if not result.ok:
        error = '\n'.join(result.errors)
        print(f'Semantic errors:\n{error}')
        return False

    hulk_code_generator(ast, result.context)

    result = subprocess.run(["gcc", "-o", "cache/main", "cache/main.c", "-lm"])
    result = subprocess.run(["./cache/main"], capture_output=True, text=True)
    print(result.stdout)

    return True
