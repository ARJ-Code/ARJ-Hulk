from .analyzer import ManyAnalyzer, NoneOrManyAnalyzer, DigitAnalyzer, AlphaNumericAnalyzer, AlphaAnalyzer, AsciiCharAnalyzer, ScapedCharAnalyzer, AndNextAnalyzer, OrAnalyzer, ConditionalAnalyzer, Between, PatternAnalyzer, or_patterns
from .lexer import Lexer
from hulk_core.token import TokenType
from hulk_core.hulk_constants import RESERVED_WORDS, SPECIAL_TOKENS, NUMERIC_CONSTANTS, DEFINED_FUNCTIONS

simple_number_analyzer = ManyAnalyzer(DigitAnalyzer())
number_analyzer = AndNextAnalyzer(simple_number_analyzer, ConditionalAnalyzer(
    AndNextAnalyzer(or_patterns('.', 'e', 'e+', 'e-'), simple_number_analyzer)))

string_analyzer1 = Between(PatternAnalyzer('\"'),
                           OrAnalyzer(ScapedCharAnalyzer(), AsciiCharAnalyzer()), PatternAnalyzer('\"'))
string_analyzer2 = Between(PatternAnalyzer('\''),
                           OrAnalyzer(ScapedCharAnalyzer(), AsciiCharAnalyzer()), PatternAnalyzer('\''))

string_analyzer = OrAnalyzer(string_analyzer1, string_analyzer2)

space_and_endline_analyzer = or_patterns(' ', '\n')
simple_comments_analyzer = Between(PatternAnalyzer(
    "//"), AsciiCharAnalyzer(), PatternAnalyzer('\n'))
complex_comments_analyzer = Between(PatternAnalyzer(
    "/*"),  AsciiCharAnalyzer(), PatternAnalyzer('*/'))
ignore_analyzer = ManyAnalyzer(OrAnalyzer(
    space_and_endline_analyzer, simple_comments_analyzer, complex_comments_analyzer))

identifier_analyzer = AndNextAnalyzer(
    AlphaAnalyzer(), NoneOrManyAnalyzer(AlphaNumericAnalyzer()))

special_token_analyzer = or_patterns(SPECIAL_TOKENS)


def identifier_analyzer_token(s: str):
    if s in RESERVED_WORDS:
        return TokenType.RESERVED_WORD
    if s in NUMERIC_CONSTANTS:
        return TokenType.NUMERIC_CONSTANT
    if s in DEFINED_FUNCTIONS:
        return TokenType.DEFINED_FUNCTION
    return TokenType.IDENTIFIER


hulk_lexer = Lexer((identifier_analyzer_token, identifier_analyzer),
                   (TokenType.NUMBER, number_analyzer),
                   (TokenType.SPECIAL_TOKEN, special_token_analyzer),
                   (TokenType.STRING, string_analyzer),
                   ignore_analyzer=ignore_analyzer)
