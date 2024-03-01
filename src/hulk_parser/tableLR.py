from .grammar import Grammar, GrammarToken, GrammarProduction
from typing import List, Tuple, Dict
from abc import ABC, abstractmethod
from enum import Enum
import json


class Action(Enum):
    SHIFT = 0,
    REDUCE = 1,
    ACCEPT = 2,
    ERROR = 3

class NodeAction:
    def __init__(self, ind: int) -> None:
        self.ind = ind
        self.terminal_actions: Dict[GrammarToken, Tuple[Action, int]] = {}
        self.no_terminal_actions: Dict[GrammarToken, int] = {}

    def add_terminal_action(self, token: GrammarToken, action: Action, ind: int):
        self.terminal_actions[token] = action, ind

    def add_no_terminal_action(self, token: GrammarToken, ind: int):
        self.no_terminal_actions[token] = ind

    def to_json(self):
        return {
            "ind": self.ind,
            "terminal_actions": {str(key): (value[0].name, value[1]) for key, value in self.terminal_actions.items()},
            "no_terminal_actions": {str(key): value for key, value in self.no_terminal_actions.items()}
        }

    def from_json(data: Dict) -> 'NodeAction':
        ind = data["ind"]
        node_action = NodeAction(ind)

        for key, value in data["terminal_actions"].items():
            node_action.add_terminal_action(
                GrammarToken(key), value[0], value[1])

        for key, value in data["no_terminal_actions"].items():
            node_action.add_no_terminal_action(GrammarToken(key), value)

        return node_action

class TableLR:
    def __init__(self, grammar: Grammar) -> None:
        self.grammar: Grammar = grammar
        self.stack_states: List[int] = [0]
        self.node_actions: List[NodeAction] = []

    def build(self, node_actions: List[NodeAction]):
        cache_json = json.dumps([node_action.to_json()
                                for node_action in node_actions])

        with open("cache.json", "w") as file:
            file.write(cache_json)

    def load(self):
        cache = json.load(open("cache.json"))
        self.node_actions = [NodeAction.from_json(x) for x in cache]

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

    def action_shift(self, action: Action, ind: int) -> Tuple[Action, int]:
        self.stack_states.append(ind)

        return action, -1

    def action_reduce(self, action: Action, ind: int) -> Tuple[Action, int]:
        production = self.grammar.get_production(ind)

        for _ in range(len(production.body)):
            self.stack_states.pop()

        self.stack_states.append(
            self.node_actions[self.stack_states[-1]].no_terminal_actions[production.head])

        return action, ind
