from compiler_tools.grammar import GrammarToken
from compiler_tools.parser import Parser
from compiler_tools.parser_out import ParseResult
from compiler_tools.automatonSLR1 import AutomatonSLR1
from compiler_tools.tableLR import TableLR
from typing import List
from .regex_grammar import regex_grammar
from .regex_core import RegexToken


def regex_build() -> bool:
    a = AutomatonSLR1('regex', regex_grammar)
    return a.ok


def regex_parser(l: List[GrammarToken]) -> ParseResult:
    t = TableLR(regex_grammar)
    t.load('regex')
    return Parser(regex_grammar, t).parse(l)

def regex_to_grammar(token: RegexToken) -> GrammarToken:
    if token.is_special:
        return [t for t in regex_grammar.terminals if t.value == token.value][0]

    return [t for t in regex_grammar.terminals if t.value == 'ch'][0]
