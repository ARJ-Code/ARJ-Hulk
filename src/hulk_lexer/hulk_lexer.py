from regex.regex import RegexBuilder, Regex
from hulk_lexer.lexer import Lexer
from hulk_core.hulk_constants import SPECIAL_TOKENS, RESERVED_WORDS

builder = RegexBuilder()


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

ignore_regex = get_regex('( |\n|\t)+|//[^\n]*\n')

hulk_lexer = Lexer(reserved_words_regex+special_tokens_regex +
                   [('NUMBER', num_regex),
                    ('STRING', string_regex),
                    ('IDENTIFIER', identifier_regex)], ignore_regex=ignore_regex)

# int_number_analyzer = AndNextAnalyzer(
#     DigitAnalyzerNotZero(), ManyAnalyzer(DigitAnalyzer()))
# number_analyzer = AndNextAnalyzer(OrAnalyzer(int_number_analyzer, PatternAnalyzer('0')), ConditionalAnalyzer(
#     AndNextAnalyzer(or_patterns('.', 'e', 'e+', 'e-'), ManyAnalyzer(DigitAnalyzer()))))

# string_analyzer1 = Between(PatternAnalyzer('\"'),
#                            OrAnalyzer(ScapedCharAnalyzer(), AsciiCharAnalyzer()), PatternAnalyzer('\"'))
# string_analyzer2 = Between(PatternAnalyzer('\''),
#                            OrAnalyzer(ScapedCharAnalyzer(), AsciiCharAnalyzer()), PatternAnalyzer('\''))

# string_analyzer = OrAnalyzer(string_analyzer1, string_analyzer2)

# space_and_endline_analyzer = or_patterns(' ', '\n', '\t')
# simple_comments_analyzer = Between(PatternAnalyzer(
#     "//"), AsciiCharAnalyzer(), PatternAnalyzer('\n'))
# complex_comments_analyzer = Between(PatternAnalyzer(
#     "/*"),  AsciiCharAnalyzer(), PatternAnalyzer('*/'))
# ignore_analyzer = ManyAnalyzer(OrAnalyzer(
#     space_and_endline_analyzer, simple_comments_analyzer, complex_comments_analyzer))

# identifier_analyzer = AndNextAnalyzer(
#     OrAnalyzer(AlphaAnalyzer(), PatternAnalyzer('_')), NoneOrManyAnalyzer(OrAnalyzer(AlphaNumericAnalyzer(), PatternAnalyzer('_'))))

# special_token_analyzer = or_patterns(SPECIAL_TOKENS)
# reserved_word_analyzer = or_patterns(RESERVED_WORDS)
# numeric_constant_analyzer = or_patterns(NUMERIC_CONSTANTS)
# defined_functions_analyzer = or_patterns(DEFINED_FUNCTIONS)


# hulk_lexer = Lexer((TokenType.RESERVED_WORD, reserved_word_analyzer),
#                    (TokenType.DEFINED_FUNCTION, defined_functions_analyzer),
#                    (TokenType.NUMERIC_CONSTANT, numeric_constant_analyzer),
#                    (TokenType.IDENTIFIER, identifier_analyzer),
#                    (TokenType.NUMBER, number_analyzer),
#                    (TokenType.SPECIAL_TOKEN, special_token_analyzer),
#                    (TokenType.STRING, string_analyzer),
#                    ignore_analyzer=ignore_analyzer)
