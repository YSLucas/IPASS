import random
from random import choice
import numpy as np
import time

class Draft:
    
    def __init__(self, blue_moves_next=True, blue_champions=set(), red_champions=set(), move_count=0):
        self.blue_moves_next = blue_moves_next
        self.blue_champions = blue_champions
        self.red_champions = red_champions
        self.move_count = move_count
        self.actions = None

    def terminal_state(self):
        if len(self.blue_champions) == 5 and len(self.red_champions) == 5:
            return True
        else:
            return False

    def get_actions(self):
        pass

    def get_next_state(self):
        pass

class Mcts:

    def __init__(self, state=Draft(), incoming_action=None, parent=None, total_sim_reward=0
                 , visit_count=0):
        self.state = state
        self.incoming_action = incoming_action
        self.parent = parent
        self.total_sim_reward = total_sim_reward
        self.visit_count = visit_count
        self.children = []
        self.tried_actions = set()
        self.remaining_actions = self.state.get_actions()
    
    def expand(self):
        action = random.choice(self.remaining_actions)
        self.remaining_actions.remove(action)
        child = Mcts(self.state.get_next_state(action), action, self)
        self.children.append(child)
        return child

def bestChild(node, cp):
    """
    return: 
    """

def expand(node):
    """
    docstring
    """
    pass

def treePolicy( node):
    """
    docstring
    """
    pass

def defaultPolicy(s):
    """
    docstring
    """
    pass

def uctSearch(parameter_list):
    """
    docstring
    """
    pass

def backup(node, delta):
    """
    docstring
    """
    pass
