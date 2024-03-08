from .regex_grammar import regex_special_tokens
from typing import List
from .regex_core import RegexResult, RegexToken

def lexer(text: str) -> RegexResult[List[RegexToken]]:
    result = []
    scape = False

    for i in range(len(text)):
        if scape:
            scape = False
            continue

        if text[i] == '\\':
            if i+1 == len(text):
                return RegexResult[List[RegexToken]](error=f'Invalid character \\: pos {i}')
            else:
                result.append(RegexToken(text[i+1], i+1))

            scape = True

            continue

        result.append(RegexToken(text[i], i, text[i] in regex_special_tokens))

    return RegexResult[List[RegexToken]](result)
