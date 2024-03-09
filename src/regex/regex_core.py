from typing import Generic, TypeVar

T = TypeVar('T')


class RegexResult(Generic[T]):
    def __init__(self, value: T | None = None, error: str = '') -> None:
        self.value: T | None = value
        self.ok: bool = value is not None
        self.error: str = error

class RegexToken():
    def __init__(self, value: str, pos: int, is_special: bool = False) -> None:
        self.value: str = value
        self.is_special = is_special
        self.pos = pos

    def __str__(self) -> str:
        return str(self.value)
