from compiler_tools.automatonLR1 import AutomatonLR1
from .hulk_grammar import hulk_grammar
from compiler_tools.grammar import GrammarToken
from compiler_tools.parser import Parser, ParseResult
from compiler_tools.tableLR import TableLR
from compiler_tools.lexer import LexerToken
from .hulk_constants import *
from typing import List


def hulk_parser_build() -> bool:
    a = AutomatonLR1('hulk', hulk_grammar)
    return a.ok


def hulk_parse(tokens: List[GrammarToken]) -> ParseResult:
    t = TableLR(hulk_grammar)
    t.load('hulk')

    p = Parser(hulk_grammar, t)

    return p.parse(tokens)


def hulk_to_grammar(token: LexerToken) -> GrammarToken:
    if token.value in SPECIAL_TOKENS or token.value in RESERVED_WORDS:
        return GrammarToken(token.value, True)

    if token.type == STRING:
        return GrammarToken('str', True)

    if token.type == NUMBER:
        return GrammarToken('num', True)

    if token.type == IDENTIFIER:
        return GrammarToken('id', True)

    if token.type == BOOLEAN:
        return GrammarToken('bool', True)
