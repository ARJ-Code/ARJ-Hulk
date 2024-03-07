from .regex_grammar import RegexGrammar
from .regex_parser import RegexParser
from .regex_core import RegexResult, RegexToken
from .regex_lexer import lexer
from typing import List


class Regex():
    def __init__(self, text: str) -> None:
        self.grammar: RegexGrammar = RegexGrammar()
        self.parser: RegexParser = RegexParser(self.grammar.grammar)
        self.error: str = ''

    def build(self) -> bool:
        return self.parser.build()

    def __regex(self, text: str) -> bool:
        result = self.__lexer(text)
        if not result.ok:
            self.error = result.error
            return False

        # result=self.__parser.parser()

    def __lexer(self, text) -> RegexResult[List[RegexToken]]:
        return lexer(text)

    def __parser(self, tokens: List[RegexToken]):
        tokens = [self.grammar.regex_to_grammar(t) for t in tokens]

        result = self.parser.parse(tokens)
