from abc import ABC, abstractmethod


class MatchResult():
    def __init__(self, value: str | None = None, error: str = '') -> None:
        self.value: str | None = value
        self.ok = value is not None
        self.error: str = error


class RegexAst(ABC):
    @abstractmethod
    def match(self, text: str, index: int = 0) -> MatchResult:
        pass


class RegexOr(RegexAst):
    def __init__(self, left: RegexAst, right: RegexAst) -> None:
        super().__init__()
        self.left: RegexAst = left
        self.right: RegexAst = right

    def match(self, text: str, index: int = 0) -> MatchResult:
        result = self.left.match(text, index)
        if result.ok:
            return result

        return self.right.match(text, index)


class RegexConcat(RegexAst):
    def __init__(self, left: RegexAst, right: RegexAst) -> None:
        super().__init__()
        self.left: RegexAst = left
        self.right: RegexAst = right

    def match(self, text: str, index: int = 0) -> MatchResult:
        left = self.left.match(text, index)
        if not left.ok:
            return left

        right = self.right.match(text, index+len(left.value))
        if not right.ok:
            return right

        return MatchResult(left.value+right.value)


class RegexQuestion(RegexAst):
    def __init__(self, body: RegexAst) -> None:
        super().__init__()

        self.body: RegexAst = body

    def match(self, text: str, index: int = 0) -> MatchResult:
        result = self.body.match(text, index)
        if result.ok:
            return result

        return MatchResult('')


class RegexMany(RegexAst):
    def __init__(self, body: RegexAst) -> None:
        super().__init__()

        self.body: RegexAst = body

    def match(self, text: str, index: int = 0) -> MatchResult:
        q = ''
      
        while index != len(text):
            result = self.body.match(text, index)
            if not result.ok:
                break

            q += result.value
            index += len(result.value)
       
        return MatchResult(q)


class RegexOneAndMany(RegexAst):
    def __init__(self, body: RegexAst) -> None:
        super().__init__()

        self.body: RegexAst = body

    def match(self, text: str, index: int = 0) -> MatchResult:
        return RegexConcat(self.body, RegexMany(self.body)).match(text, index)


class RegexChar(RegexAst):
    def __init__(self, char: str) -> None:
        super().__init__()

        self.char: str = char

    def match(self, text: str, index: int = 0) -> MatchResult:
        if index < len(text) and text[index] == self.char:
            return MatchResult(self.char)

        return MatchResult(error='Invalid character')


class RegexAnyChar(RegexAst):
    def match(self, text: str, index: int = 0) -> MatchResult:
        if index < len(text) and text[index] == self.char:
            return MatchResult(text[index])

        return MatchResult(error='Invalid character')


class RegexRank(RegexAst):
    def __init__(self, left: str, right: str) -> None:
        super().__init__()

        self.left: str = left
        self.right: str = right

    def match(self, text: str, index: int = 0) -> MatchResult:
        if index < len(text) and ord(self.left) <= ord(text[index]) and ord(text[index]) <= ord(self.right):
            return MatchResult(text[index])

        return MatchResult(error='Invalid character')


class RegexNot(RegexAst):
    def __init__(self, body: RegexAst) -> None:
        super().__init__()

        self.body: RegexAst = body

    def match(self, text: str, index: int = 0) -> MatchResult:
        if index < len(text) and not self.body.match(text, index).ok:
            return MatchResult(text[index])

        return MatchResult(error='Invalid character')
