from enum import Enum


class TokenType(Enum):
    IDENTIFIER = 0,
    NUMBER = 1,
    STRING = 2,
    SPECIAL_TOKEN = 3,


class Token:
    def __init__(self, row: int, col: int, value: str, token_type: TokenType) -> None:
        self.value = value
        self.row = row
        self.col = col
        self.type = token_type
