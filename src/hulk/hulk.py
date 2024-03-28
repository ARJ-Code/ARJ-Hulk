from hulk.hulk_semantic_check import SemanticChecker, TypeBuilder, TypeCollector
from hulk.hulk_semantic_tools import Scope
from .hulk_lexer import hulk_lexer_build
from .hulk_parser import hulk_parser_build, hulk_to_grammar, hulk_parse
from compiler_tools.lexer import Lexer
from .hulk_grammar import hulk_grammar
from .hulk_code_generator import hulk_code_generator


def hulk_build() -> bool:
    hulk_lexer_build()
    return hulk_parser_build()


def hulk_compile_str(program: str) -> bool:
    hulk_lexer = Lexer()
    hulk_lexer.load('hulk')

    result = hulk_lexer.run(program)
    tokens = result.tokens

    result = hulk_parse([hulk_to_grammar(t) for t in result.tokens])

    if result.ok:

        ast = hulk_grammar.evaluate(result.derivation_tree, tokens)

        errors = []

        collector = TypeCollector(errors)
        collector.visit(ast)

        context = collector.context

        builder = TypeBuilder(context, errors)
        builder.visit(ast)

        scope = Scope()

        semantic_checker = SemanticChecker(context, errors)
        semantic_checker.visit(ast, scope)

        print('Errors:', errors)
        # print('Context:')
        # print(context)

        return errors == []

        # hulk_code_generator(ast)

    return result.ok


def hulk_compile():

    f = open('cache/main.hulk')
    p = f.read()
    f.close()

    print(hulk_compile_str(p))
