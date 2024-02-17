from enum import Enum


class TokenType(Enum):
    IDENTIFIER = 0,
    NUMBER = 1,
    STRING = 2,
    SPECIAL_TOKEN = 3,
    RESERVED_WORD = 4,
    DEFINED_FUNCTION = 5,
    NUMERIC_CONSTANT = 6


class Token:
    def __init__(self, row: int, col: int, value: str, token_type: TokenType) -> None:
        self.value = value
        self.row = row
        self.col = col
        self.type = token_type

    def __compare_by_value():
        return [TokenType.DEFINED_FUNCTION, TokenType.NUMERIC_CONSTANT, TokenType.SPECIAL_TOKEN, TokenType.RESERVED_WORD]

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Token):
            return False

        if self.type in self.__compare_by_value():
            return self.type == __value.type and self.value == __value.value
