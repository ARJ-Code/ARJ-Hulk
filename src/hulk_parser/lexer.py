from typing import List
from .analyzer import Analyzer
from hulk_core.error import ParsingError


def lexer(string: str, analyzers: List[Analyzer]):
    pos = 0
    row = 0
    col = 0

    tokens = []

    while (len(string) != pos):
        can_analyze = False

        for analyzer in analyzers:
            if (analyzer.can_analyze(string, pos)):
                r = analyzer.run(string, pos, row, col)

                pos, row, col = r.pos, r.row, r.col

                if (not r.ok):
                    return r.error

                if (r.token is not None):
                    tokens.append(r.token)

                can_analyze = True
                break

        if (not can_analyze):
            return ParsingError('', row, col)

    return tokens
