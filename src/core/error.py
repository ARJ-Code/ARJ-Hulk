class Error:
    def __init__(self,msg:str,pos_x:int,pos_y:int) -> None:
        self.msg=msg
        self.pos_x=pos_x
        self.pos_y=pos_y

class ParsingError(Error):
    def __init__(self, msg: str, pos_x: int, pos_y: int) -> None:
        super().__init__(msg, pos_x, pos_y)


        