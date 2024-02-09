from .analyzer import ManyAnalyzer, DigitAnalyzer, AlphaNumericAnalyzer, AlphaAnalyzer, AsciiCharAnalyzer, ScapedCharAnalyzer, AndAnalyzer, OrAnalyzer, ConditionalAnalyzer, Between, PatternAnalyzer, or_patterns
from .lexer import Lexer
from hulk_core.token import TokenType

simple_number_analyzer = ManyAnalyzer(DigitAnalyzer())
number_analyzer = AndAnalyzer(simple_number_analyzer, ConditionalAnalyzer(
    or_patterns('.', 'e', 'e+', 'e-'), simple_number_analyzer))

string_analyzer = Between(PatternAnalyzer('\"'),
                          OrAnalyzer(ScapedCharAnalyzer(), AsciiCharAnalyzer()), PatternAnalyzer('\"'))
char_analyzer = Between(PatternAnalyzer('\''), OrAnalyzer(
    ScapedCharAnalyzer(), AsciiCharAnalyzer()), PatternAnalyzer('\''))

space_and_endline_analyzer = or_patterns(' ', '\n')
simple_comments_analyzer = Between(PatternAnalyzer(
    "//"), AsciiCharAnalyzer(), PatternAnalyzer('\n'))
complex_comments_analyzer = Between(PatternAnalyzer(
    "/*"),  AsciiCharAnalyzer(), PatternAnalyzer('*/'))
ignore_analyzer = ManyAnalyzer(OrAnalyzer(
    space_and_endline_analyzer, simple_comments_analyzer, complex_comments_analyzer))

identifier_analyzer = AndAnalyzer(
    AlphaAnalyzer(), ManyAnalyzer(AlphaNumericAnalyzer()))

special_token_analyzer = or_patterns(
    ";", ",", ".", ":", "(", ")", "[", "]", "{", "}",
    "<", ">", "=", "+", "-", "*", "/", "%", "|", "&",
    "^", "@", ">=", "<=", "==", "||", "&&", "^^", ":=",
    "=>")

hulk_lexer = Lexer((TokenType.IDENTIFIER, identifier_analyzer),
                   (TokenType.NUMBER, number_analyzer),
                   (TokenType.SPECIAL_TOKEN, special_token_analyzer),
                   (TokenType.STRING, string_analyzer),
                   ignore_analyzer=ignore_analyzer)
