from abc import ABC, abstractmethod
from hulk_core.error import ParsingError


class AnalyzerResult:
    def __init__(self, index: int, row: int, col: int, token: str | None = None, error: ParsingError | None = None) -> None:
        self.ok = error is None
        self.empty = token is None
        self.index = index
        self.row = row
        self.col = col
        self.token = "" if token is None else token
        self.error = error


class Analyzer(ABC):
    @abstractmethod
    def match(self, index: int, text: str) -> bool:
        pass

    def run(self, index: int, row: int, col: int, text: str) -> AnalyzerResult:
        if self.match(index, text):
            return self._run(index, row, col, text)

        return AnalyzerResult(index, row, col, None, ParsingError("Invalid character", row, col))

    @abstractmethod
    def _run(self, index: int, row: int, col: int, text: str) -> AnalyzerResult:
        pass

    def _ok_run(self, index: int, row: int, col: int, token: str) -> AnalyzerResult:
        for i in token:
            if i == '\n':
                row += 1
                col = 0
            else:
                col += 1
        return AnalyzerResult(index+len(token), row, col, token)


class AlphaNumericAnalyzer(Analyzer):
    def match(self, index: int, text: str) -> bool:
        return text[index].isalnum()

    def _run(self, index: int, row: int, col: int, text: str) -> AnalyzerResult:
        return self._ok_run(index, row, col, text[index])


class DigitAnalyzer(Analyzer):
    def match(self, index: int, text: str) -> bool:
        return text[index].isdigit()

    def _run(self, index: int, row: int, col: int, text: str) -> AnalyzerResult:
        return self._ok_run(index, row, col, text[index])


class PatternAnalyzer(Analyzer):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def match(self, index: int, text: str) -> bool:
        return text[index:].startswith(self.pattern)

    def _run(self, index: int, row: int, col: int, _: str) -> AnalyzerResult:
        return self._ok_run(index, row, col, self.pattern)


class OrAnalyzer(Analyzer):
    def __init__(self, *analyzers: Analyzer) -> None:
        if len(analyzers) == 1 and isinstance(analyzers[0], list):
            self.analyzers = analyzers[0]
        else:
            self.analyzers = list(analyzers)

    def match(self, index: int, text: str) -> bool:
        return any(analyzer.match(index, text) for analyzer in self.analyzers)

    def _run(self, index: int, row: int, col: int, text: str) -> AnalyzerResult:
        for analyzer in self.analyzers:
            if analyzer.match(index, text):
                return analyzer.run(index, row, col, text)

        return AnalyzerResult(index, row, col, None, ParsingError("Invalid character", row, col))


class AndAnalyzer(Analyzer):
    def __init__(self, *analyzers: Analyzer) -> None:
        if len(analyzers) == 1 and isinstance(analyzers[0], list):
            self.analyzers = analyzers[0]
        else:
            self.analyzers = list(analyzers)

    def match(self, index: int, text: str) -> bool:
        return self.analyzers[0].match(index, text)

    def _run(self, index: int, row: int, col: int, text: str) -> AnalyzerResult:
        token = ""
        for analyzer in self.analyzers:
            if analyzer.match(index, text):
                result = analyzer.run(index, row, col, text)
                if result.ok:
                    token += result.token
                    index = result.index
                    row = result.row
                    col = result.col
                else:
                    return result
            else:
                return AnalyzerResult(index, row, col, None, ParsingError("Invalid character", row, col))

        return AnalyzerResult(index, row, col, token)


class ConditionalAnalyzer:
    def __init__(self, condition: Analyzer, body: Analyzer) -> None:
        self.condition = condition
        self.body = body

    def match(self, _: int, __: str) -> bool:
        return True

    def run(self, index: int, row: int, col: int, text: str) -> AnalyzerResult:
        if self.condition.match(index, text):
            return AndAnalyzer(self.condition, self.body).run(index, row, col, text)
        return AnalyzerResult(index, row, col)


class ManyAnalyzer(Analyzer):
    def __init__(self, analyzer: Analyzer) -> None:
        self.analyzer = analyzer

    def match(self, index: int, text: str) -> bool:
        return self.analyzer.match(index, text)

    def _run(self, index: int, row: int, col: int, text: str) -> AnalyzerResult:
        token = ""
        while index != len(text) and self.analyzer.match(index, text):
            result = self.analyzer.run(index, row, col, text)
            if result.ok:
                token += result.token
                index = result.index
                row = result.row
                col = result.col
            else:
                return result

        return AnalyzerResult(index, row, col, token)


def or_patterns(*patterns: str) -> OrAnalyzer:
    if len(patterns) == 1 and isinstance(patterns[0], list):
        patterns = patterns[0]
    else:
        patterns = list(patterns)

    patterns.sort(key=len, reverse=True)

    return OrAnalyzer([PatternAnalyzer(p) for p in patterns])
