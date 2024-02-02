class Token:
    def __init__(self,pos_x,pos_y,value:int|str|float) -> None:
        self.value=value
        self.pos_x=pos_x
        self.pos_y=pos_y

class String(Token):
    def __init__(self, pos_x, pos_y, value:str) -> None:
        super().__init__(pos_x, pos_y, value)

class Int(Token):
    def __init__(self, pos_x, pos_y, value: int) -> None:
        super().__init__(pos_x, pos_y, value)

class Double(Token):
    def __init__(self, pos_x, pos_y, value: float) -> None:
        super().__init__(pos_x, pos_y, value)

class Literal(Token):
    def __init__(self, pos_x, pos_y, value: str) -> None:
        super().__init__(pos_x, pos_y, value)

class SpecialToken(Token):
    def __init__(self, pos_x, pos_y, value:  str ) -> None:
        super().__init__(pos_x, pos_y, value)

class ReservedWord(Token):
    def __init__(self, pos_x, pos_y, value: str) -> None:
        super().__init__(pos_x, pos_y, value)


