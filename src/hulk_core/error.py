class Error:
    def __init__(self, msg: str, row: int, col: int) -> None:
        self.msg = msg
        self.row = row
        self.col = col


class ParsingError(Error):
    def __init__(self, msg: str, row: int, col: int) -> None:
        super().__init__(msg, row, col)
