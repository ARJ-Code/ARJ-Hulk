class Token:
    def __init__(self,row:int,col:int,value:int|str|float) -> None:
        self.value=value
        self.row=row
        self.col=col

class String(Token):
    def __init__(self, row:int,col:int, value:str) -> None:
        super().__init__(row, col, value)

class Int(Token):
    def __init__(self, row:int,col:int, value: int) -> None:
        super().__init__(row, col, value)

class Double(Token):
    def __init__(self, row:int,col:int, value: float) -> None:
        super().__init__(row, col, value)

class Literal(Token):
    def __init__(self, row:int,col:int, value: str) -> None:
        super().__init__(row, col, value)

class SpecialToken(Token):
    def __init__(self, row:int,col:int, value:  str ) -> None:
        super().__init__(row, col, value)

class ReservedWord(Token):
    def __init__(self, row:int,col:int, value: str) -> None:
        super().__init__(row, col, value)


