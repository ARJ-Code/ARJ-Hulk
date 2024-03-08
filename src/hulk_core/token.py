from enum import Enum


class HulkToken:
    def __init__(self, row: int, col: int, value: str, token_type: str) -> None:
        self.value: str = value
        self.row: int = row
        self.col: int = col
        self.type: str = token_type

    def __eq__(self, __value: object) -> bool:
        return self.type == __value.type
