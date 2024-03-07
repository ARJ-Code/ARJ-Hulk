from .regex_grammar import RegexGrammar
from .regex_parser import RegexParser
from .regex_core import RegexResult, RegexToken
from .regex_lexer import lexer
from typing import List
from .regex_ast import RegexAst, MatchResult
from .regex_attributed_grammar import RegexAttributedGrammar


class Regex():
    def __init__(self, text: str) -> None:
        self.grammar: RegexGrammar = RegexGrammar()
        self.parser: RegexParser = RegexParser(self.grammar.grammar)
        self.error: str = ''
        self.ast: RegexAst | None = None

        self.__regex(text)

    def build(self) -> bool:
        return self.parser.build()

    def match(self, text: str, index: int) -> MatchResult:
        return self.ast.match(text, index)

    def __regex(self, text: str):
        result = self.__lexer(text)
        if not result.ok:
            self.error = result.error
            return

        result = self.__parser(result.value)

    def __lexer(self, text) -> RegexResult[List[RegexToken]]:
        return lexer(text)

    def __parser(self, tokens: List[RegexToken]) -> RegexResult[RegexAst]:
        result = self.parser.parse(
            [self.grammar.regex_to_grammar(t) for t in tokens])
        if not result.ok:
            return RegexResult[RegexAst](error=result.error)

        return RegexAttributedGrammar().to_ast(result.derivation_tree, tokens)
