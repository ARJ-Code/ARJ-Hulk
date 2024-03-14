from regex.regex import Regex
from compiler_tools.lexer import Lexer
from hulk.hulk_constants import *


def get_special_token_pattern(token: str) -> str:
    return "".join([f'\\{t}' for t in token])


def hulk_lexer_build() -> bool:
    RESERVED_WORDS.sort(key=lambda x: len(x), reverse=True)
    NUMERIC_CONSTANTS.sort(key=lambda x: len(x), reverse=True)
    DEFINED_FUNCTIONS.sort(key=lambda x: len(x), reverse=True)
    SPECIAL_TOKENS.sort(key=lambda x: len(x), reverse=True)

    special_tokens_regex = [(t, Regex(get_special_token_pattern(t)))
                            for t in SPECIAL_TOKENS]
    reserved_words_regex = [(t.upper(), Regex(t)) for t in RESERVED_WORDS]

    num_regex = Regex('0|([1-9][0-9]*)((\.|e\+|e\-|e)[0-9]+)?')

    string_regex = Regex(
        '"(\\\\[tnr"\']|[^"\\\\])*"|\'(\\\\[tnr\'"]|[^\'\\\\])*\'')

    identifier_regex = Regex('(_|[a-zA-Z])(_|[a-zA-Z0-9])*')

    boolean_regex = Regex('true|false')

    ignore_regex = Regex('( |\n|\t)+|//[^\n]*\n|/\*([^\*]|\*[^/])*(\*/|\*\*/)')

    tokens_regex = reserved_words_regex + special_tokens_regex + [(BOOLEAN, boolean_regex),
                                                                  (NUMBER,
                                                                   num_regex),
                                                                  (STRING,
                                                                   string_regex),
                                                                  (IDENTIFIER, identifier_regex)]

    tokens_automaton = [(t, r.automaton) for t, r in tokens_regex]

    Lexer().build('hulk', tokens_automaton, ignore_regex.automaton)


def hulk_lexer_load() -> Lexer:
    hulk_lexer = Lexer()
    hulk_lexer.load('hulk')

    return hulk_lexer
