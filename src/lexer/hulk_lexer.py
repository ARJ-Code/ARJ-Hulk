from .analyzer import ManyAnalyzer, NoneOrManyAnalyzer, DigitAnalyzer, DigitAnalyzerNotZero, AlphaNumericAnalyzer, AlphaAnalyzer, AsciiCharAnalyzer, ScapedCharAnalyzer, AndNextAnalyzer, OrAnalyzer, ConditionalAnalyzer, Between, PatternAnalyzer, or_patterns
from .lexer import Lexer
from hulk_core.token import TokenType
from hulk_core.hulk_constants import RESERVED_WORDS, SPECIAL_TOKENS, NUMERIC_CONSTANTS, DEFINED_FUNCTIONS

int_number_analyzer = AndNextAnalyzer(
    DigitAnalyzerNotZero(), ManyAnalyzer(DigitAnalyzer()))
number_analyzer = AndNextAnalyzer(OrAnalyzer(int_number_analyzer, PatternAnalyzer('0')), ConditionalAnalyzer(
    AndNextAnalyzer(or_patterns('.', 'e', 'e+', 'e-'), ManyAnalyzer(DigitAnalyzer()))))

string_analyzer1 = Between(PatternAnalyzer('\"'),
                           OrAnalyzer(ScapedCharAnalyzer(), AsciiCharAnalyzer()), PatternAnalyzer('\"'))
string_analyzer2 = Between(PatternAnalyzer('\''),
                           OrAnalyzer(ScapedCharAnalyzer(), AsciiCharAnalyzer()), PatternAnalyzer('\''))

string_analyzer = OrAnalyzer(string_analyzer1, string_analyzer2)

space_and_endline_analyzer = or_patterns(' ', '\n', '\t')
simple_comments_analyzer = Between(PatternAnalyzer(
    "//"), AsciiCharAnalyzer(), PatternAnalyzer('\n'))
complex_comments_analyzer = Between(PatternAnalyzer(
    "/*"),  AsciiCharAnalyzer(), PatternAnalyzer('*/'))
ignore_analyzer = ManyAnalyzer(OrAnalyzer(
    space_and_endline_analyzer, simple_comments_analyzer, complex_comments_analyzer))

identifier_analyzer = AndNextAnalyzer(
    OrAnalyzer(AlphaAnalyzer(), PatternAnalyzer('_')), NoneOrManyAnalyzer(OrAnalyzer(AlphaNumericAnalyzer(), PatternAnalyzer('_'))))

special_token_analyzer = or_patterns(SPECIAL_TOKENS)
reserved_word_analyzer = or_patterns(RESERVED_WORDS)
numeric_constant_analyzer = or_patterns(NUMERIC_CONSTANTS)
defined_functions_analyzer = or_patterns(DEFINED_FUNCTIONS)


hulk_lexer = Lexer((TokenType.RESERVED_WORD, reserved_word_analyzer),
                   (TokenType.DEFINED_FUNCTION, defined_functions_analyzer),
                   (TokenType.NUMERIC_CONSTANT, numeric_constant_analyzer),
                   (TokenType.IDENTIFIER, identifier_analyzer),
                   (TokenType.NUMBER, number_analyzer),
                   (TokenType.SPECIAL_TOKEN, special_token_analyzer),
                   (TokenType.STRING, string_analyzer),
                   ignore_analyzer=ignore_analyzer)
