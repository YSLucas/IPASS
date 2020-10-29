from logging import NullHandler
import random
from random import choice
import numpy as np
import time
import pickle

MODEL_PATH = 'models/lr_model_1.pkl'

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
        self.total_sim_reward = total_sim_reward # Q(v)
        self.visit_count = visit_count # N(v)
        self.children = []
        self.tried_actions = set()
        self.remaining_actions = self.state.get_actions()
    
    def expand(self):
        action = random.choice(self.remaining_actions)
        self.remaining_actions.remove(action)
        child = Mcts(self.state.get_next_state(action), action, self)
        self.children.append(child)
        return child # v'

def lrModel(s):
    """
    return:
    """
    model = pickle.load(open(MODEL_PATH, 'rb'))
    

def bestChild(node, c):
    """
    return: 
    max(   Q(v') / N(v')   
        +  c *  sqrt( ( 2 ln N(v) ) / N(v') ) 
        )
    """
    return max (
                (node.total_sim_reward / node.visit_count) # exploitation
                + c * np.sqrt( 1 / node.visit_count)       # exploration
               )

def treePolicy(node, c):
    """
    docstring
    """
    while node.is_terminal() is False:
        if len(node.remaining_actions) != 0:
            return node.expand()
        else:
            node = node.bestChild(node, c)
    return node

def defaultPolicy(s, model):
    """
    docstring
    Add compute_rewards() into this function
    """
    while s.is_terminal() is False:
        pre = s.get_actions()
        a = random.choice(pre)
        s = s.get_next_state(a)
    return lrModel(s)

def uctSearch(time_limit,):
    """
    docstring
    """
    while time_limit > time:
        pass

def backup(node, delta):
    """
    docstring
    """
    while node is not None:
        node.visit_count += 1
        node.total_sim_reward += delta
        delta -= delta  # niet zeker of deze line klopt
        node = node.parent
