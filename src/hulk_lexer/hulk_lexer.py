from regex.regex import builder, Regex
from hulk_lexer.lexer import Lexer
from hulk_core.hulk_constants import SPECIAL_TOKENS, RESERVED_WORDS


def get_special_token_pattern(token: str) -> str:
    return "".join([f'\\{t}' for t in token])


def get_regex(pattern: str) -> Regex:
    return builder.parse(pattern).value


RESERVED_WORDS.sort(key=lambda x: len(x), reverse=True)
SPECIAL_TOKENS.sort(key=lambda x: len(x), reverse=True)

special_tokens_regex = [(t, get_regex(get_special_token_pattern(t)))
                        for t in SPECIAL_TOKENS]
reserved_words_regex = [(t.upper(), get_regex(t)) for t in RESERVED_WORDS]

num_regex = get_regex('0|([1-9][0-9]*)((\.|e\+|e\-|e)[0-9]+)?')

string_regex = get_regex('"(\\\\[tnr"]|[^"])*"|\'(\\\\[tnr\']|[^\'])*\'')

identifier_regex = get_regex('(_|[a-zA-Z])(_|[a-zA-Z0-9])*')

ignore_regex = get_regex('( |\n|\t)+|//[^\n]*\n|/\*[^(\*/)]*\*/')

hulk_lexer = Lexer(reserved_words_regex+special_tokens_regex +
                   [('NUMBER', num_regex),
                    ('STRING', string_regex),
                    ('IDENTIFIER', identifier_regex)], ignore_regex=ignore_regex)
