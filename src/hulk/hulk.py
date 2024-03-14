from .hulk_lexer import hulk_lexer_build
from .hulk_parser import hulk_parser_build


def hulk_build() -> bool:
    hulk_lexer_build()
    return hulk_parser_build()
