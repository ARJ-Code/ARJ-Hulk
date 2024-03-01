from .grammar import Grammar, GrammarToken, GrammarProduction
from typing import List, Tuple, Dict
from abc import ABC, abstractmethod
from enum import Enum


class Action(Enum):
    SHIFT = 0,
    REDUCE = 1,
    ACCEPT = 2,
    ERROR = 3


class ItemLR:
    def __init__(self, production: GrammarProduction, index: int) -> None:
        self.production: GrammarProduction = production
        self.index: int = index


class NodeLR:
    def __init__(self, ind: int) -> None:
        self.ind: int = ind
        self.items: List[ItemLR] = []
        self.transitions: Dict[GrammarToken, 'NodeLR'] = {}

    def add_item(self, item: ItemLR) -> None:
        self.items.append(item)

    def add_transition(self, token: GrammarToken, node: 'NodeLR') -> None:
        self.transitions[token] = node


class NodeAction:
    def __init__(self, ind: int) -> None:
        self.ind = ind
        self.terminal_actions: Dict[GrammarToken, Tuple[Action, int]] = {}
        self.no_terminal_actions: Dict[GrammarToken, int] = {}

    def add_terminal_action(self, token: GrammarToken, action: Action, ind: int) -> None:
        self.terminal_actions[token] = action, ind

    def add_no_terminal_action(self, token: GrammarToken, ind: int) -> None:
        self.no_terminal_actions[token] = ind

    

class AutomatonLR(ABC):
    def __init__(self, grammar: Grammar) -> None:
        self.grammar: Grammar = grammar
        self.stack_states: List[int] = [0]
        self.node_actions: List[NodeAction] = []

    @abstractmethod
    def build():
        pass

    @abstractmethod
    def load():
        pass

    def action(self, token: GrammarToken) -> Tuple[Action, int]:
        node = self.node_actions[self.stack_states[-1]]

        if token in node.terminal_actions:
            action, ind = node.terminal_actions[token]

            if action == Action.SHIFT:
                return self.action_shift(action, ind)
                
            if action == Action.REDUCE:
                return self.action_reduce(action, ind)
                
            if action == Action.ACCEPT:
                return action, -1

        return Action.ERROR, -1
    
    def action_shift(self,action:Action,ind:int)->Tuple[Action,int]:
        self.stack_states.append(ind)

        return action, -1

    def action_reduce(self,action:Action,ind:int)->Tuple[Action,int]:
        production = self.grammar.get_production(ind)

        for _ in range(len(production.body)):
            self.stack_states.pop()

        self.stack_states.append(
            self.node_actions[self.stack_states[-1]].no_terminal_actions[production.head])

        return action, ind
