from .analyzer import ManyAnalyzer, NoneOrManyAnalyzer, DigitAnalyzer, AlphaNumericAnalyzer, AlphaAnalyzer, AsciiCharAnalyzer, ScapedCharAnalyzer, AndNextAnalyzer, OrAnalyzer, ConditionalAnalyzer, Between, PatternAnalyzer, or_patterns
from .lexer import Lexer
from hulk_core.token import TokenType

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
