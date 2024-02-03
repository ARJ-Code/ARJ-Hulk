from abc import ABC, abstractmethod
from hulk_core.token import Token, Int, Double, String, Char
from hulk_core.error import ParsingError

scaped_char = {'n': '\n', 't': '\t', 'r': '\r',
               '\\': '\\', '\"': '\"', '\'': '\''}

special_token = [',', ';', '(', ')', '[', ']', '{', '}', '+', '-', '*', '/']

space_token = [' ', '\n']

stop_char = [x[0] for x in special_token+space_token]

class AnalyzerResult:
    def __init__(self, pos: int, row: int, col: int, token: Token | None = None, error: ParsingError | None = None) -> None:
        self.ok = error is None
        self.row = row
        self.col = col
        self.pos = pos
        self.token = token
        self.error = error


class Analyzer(ABC):
    @abstractmethod
    def can_analyze(self, string: str, pos: int) -> bool:
        pass

    @abstractmethod
    def run(self, string: str, pos: int, row: int, col: int) -> AnalyzerResult:
        pass


class SpaceAnalyzer(Analyzer):
    def can_analyze(self, string: str, pos: int) -> bool:
        return string[pos] == ' ' or string[pos] == '\n'

    def run(self, string: str, pos: int, row: int, col: int) -> AnalyzerResult:
        while (len(string) != pos and string[pos] in space_token):
            row += 1 if string[pos] == '\n' else 0
            col = col+1 if string[pos] != '\n' else 0
            pos += 1

        return AnalyzerResult(pos, row, col)


class NumberAnalyzer(Analyzer):
    def can_analyze(self, string: str, pos: int) -> bool:
        return string[pos].isdigit()

    def run(self, string: str, pos: int, row: int, col: int) -> AnalyzerResult:
        result = ''
        is_decimal = False
        decimal_char = ['e', '.']

        while (len(string) != pos):
            is_decimal_char = string[pos] in decimal_char

            if (is_decimal_char):
                if (is_decimal):
                    return AnalyzerResult(pos, row, col, error=ParsingError('', row, col))
                else:
                    is_decimal = True

            if (not is_decimal and string[pos] in stop_char):
                break

            if (not is_decimal_char and not string[pos].isdigit()):
                return AnalyzerResult(pos, row, col, error=ParsingError('', row, col))

            result += string[pos]
            col += 1
            pos += 1

        return AnalyzerResult(pos, row, col, token=Double(row, col, float(result)) if is_decimal else Int(row, col, int(result)))

class ScapedCharAnalyzer(Analyzer):
    def can_analyze(self, string: str, pos: int) -> bool:
        return string[pos]=='\\'
    
    def run(self, string: str, pos: int, row: int, col: int) -> AnalyzerResult:
        if (pos == len(string)-1):
            return AnalyzerResult(pos, row, col, error=ParsingError('', row, col))

        pos += 1
        col += 1

        if(not string[pos] in scaped_char):
            return AnalyzerResult(pos,row,col,error=ParsingError('',row,col))
        
        return AnalyzerResult(pos,row,col,token=Char(row,col,scaped_char[string[pos]]))


class StringAnalyzer(Analyzer):
    def can_analyze(self, string: str, pos: int) -> bool:
        return string[pos] == '\"'

    def run(self, string: str, pos: int, row: int, col: int) -> AnalyzerResult:
        scaped_char_analyzer=ScapedCharAnalyzer()

        if (string[pos] != '\"'):
            return AnalyzerResult(pos, row, col, error=ParsingError('', row, col))

        pos += 1
        col += 1

        result = ''

        while (string[pos] != '\"'):
            if (scaped_char_analyzer.can_analyze(string,pos)):
                r=scaped_char_analyzer.run(string,pos,row,col)
                if(r.ok):
                    result+=r.token.value
                    pos,row,col=r.pos,r.row,r.col
                else:
                    return r.error
            else:
                result += string[pos]
            col += 1
            pos += 1

            if (len(string) == pos):
                return AnalyzerResult(pos, row, col, error=ParsingError('', row, col))

        pos += 1
        col += 1

        return AnalyzerResult(pos, row, col, token=String(row, col, result))
    
class CharAnalyzer(Analyzer):
    def can_analyze(self, string: str, pos: int) -> bool:
        return string[pos]=='\''
    
    def run(self, string: str, pos: int, row: int, col: int) -> AnalyzerResult:
        scaped_char_analyzer=ScapedCharAnalyzer()

        if (string[pos] != '\''):
            return AnalyzerResult(pos, row, col, error=ParsingError('', row, col))

        pos += 1
        col += 1

        result = ''

        if (scaped_char_analyzer.can_analyze(string,pos)):
            r=scaped_char_analyzer.run(string,pos,row,col)
            if(r.ok):
                result+=r.token.value
            else:
                return r.error
        else:
            result += string[pos]
           

        if (len(string) == pos or string[pos]!='\''):
            return AnalyzerResult(pos, row, col, error=ParsingError('', row, col))

        pos += 1
        col += 1

        return AnalyzerResult(pos, row, col, token=String(row, col, result))
    
