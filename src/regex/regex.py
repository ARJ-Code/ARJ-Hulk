from .regex_grammar import RegexGrammar
from .regex_parser import RegexParser
from .regex_core import RegexResult, RegexToken
from .regex_lexer import lexer
from typing import List
from .regex_ast import RegexAst, MatchResult
from .regex_attributed_grammar import RegexAttributedGrammar


class Regex():
    def __init__(self, ast: RegexAst) -> None:
        self.ast: RegexAst = ast

    def match(self, text: str, index: int = 0) -> MatchResult:
        return self.ast.match(text, index)


class RegexBuilder():
    def __init__(self) -> None:
        self.grammar: RegexGrammar = RegexGrammar()
        self.parser: RegexParser = RegexParser(self.grammar.grammar)
        self.error: str = ''

    def parse(self, text: str) -> RegexResult[Regex]:
        result = self.__lexer(text)
        if not result.ok:
            return RegexResult[Regex](error=result.error)

        result = self.__parser(result.value)
        if not result.ok:
            return RegexResult[Regex](error=result.error)

        return RegexResult[Regex](Regex(result.value))

    def build(self) -> bool:
        return self.parser.build()

    def __lexer(self, text) -> RegexResult[List[RegexToken]]:
        return lexer(text)

    def __parser(self, tokens: List[RegexToken]) -> RegexResult[RegexAst]:
        result = self.parser.parse(
            [self.grammar.regex_to_grammar(t) for t in tokens])

        if not result.ok:
            return RegexResult[RegexAst](error=result.error)

        return RegexAttributedGrammar().to_ast(result.derivation_tree, tokens)
