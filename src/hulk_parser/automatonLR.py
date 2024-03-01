from .grammar import Grammar, GrammarToken
from typing import List, Tuple
from abc import ABC, abstractmethod
from enum import Enum


class Action(Enum):
    SHIFT = 0,
    REDUCE = 1,
    ACCEPT = 2,
    ERROR = 3


class AutomatonLR(ABC):
    def __init__(self, grammar: Grammar) -> None:
        self.grammar: Grammar = grammar
        self.stack_states: List[int] = []

    @abstractmethod
    def build():
        pass

    @abstractmethod
    def load():
        pass

    @abstractmethod
    def action(stack_tokens: List[GrammarToken], input: GrammarToken) -> Tuple[Action, int]:
        pass
