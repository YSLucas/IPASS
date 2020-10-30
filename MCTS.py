import random
from random import choice
import numpy as np
import time
import pickle

MODEL_PATH = 'models/lr_model_1.pkl'

"""
Dit algoritme is gemodelleerd naar
 de pseudocode van Monte Carlo Tree Search UCT (http://ccg.doc.gold.ac.uk/ccg_old/teaching/ludic_computing/ludic16.pdf).

variabele in de pseudocode:
v    = node
v'   = child
v0   = root node
s    = state
c    = "Exploration term C balances exploration vs exploitation" 
a    = action
N(v) = visit count
Q(v) = total simulation reward
"""

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
        self.state = state # s
        self.incoming_action = incoming_action
        self.parent = parent
        self.total_sim_reward = total_sim_reward # Q(v)
        self.visit_count = visit_count # N(v)
        self.children = []
        self.tried_actions = set()
        self.remaining_actions = self.state.get_actions()
    
    # def expand(self):
    #     action = random.choice(self.remaining_actions)
    #     self.remaining_actions.remove(action)
    #     child = Mcts(self.state.get_next_state(action), action, self)
    #     self.children.append(child)
    #     return child # v'

def lrModel(s):
    """
    return:
    """
    model = pickle.load(open(MODEL_PATH, 'rb'))

def expand(node):
    """
    Variables:
    v, v', a, s, 
    """
    action = random.choice(node.remaining_actions)
    node.remaining_actions.remove(action)
    child = Mcts(node.state.get_next_state(action), action, node)
    node.children.append(child)
    return child # v'
 

def bestChild(node, c):
    """
    Variables:
    v, v', N(v), N(v'), Q(v'), c
    
    return: 
    max(   
            ( Q(v') / N(v') ) +  c *  sqrt( ( 2ln N(v) ) / N(v') ) 
        )
    """
    child = node.children() # [v']
    res = []
    for x in child:
        res.append(
        (x.total_sim_reward / x.visit_count) # exploitation
        + c * np.sqrt( ( 2 * np.log(node.visit_count) ) / x.visit_count) # exploration
        ) 
    
    return max(res)

    # return max (
    #             (child.total_sim_reward / child.visit_count) # exploitation
    #             + c * np.sqrt( (np.log(2) * node.visit_count) / child.visit_count)       # exploration
    #            )

def treePolicy(node, c):
    """
    variables:
    v, c
    """
    while node.is_terminal() is False:
        if len(node.remaining_actions) != 0:
            return node.expand()
        else:
            node = node.bestChild(node, c) # v
    return node

def defaultPolicy(s, model):
    """
    Variables:
    s, a
    """
    while s.is_terminal() is False:
        pre = s.get_actions()
        a = random.choice(pre) # a
        s = s.get_next_state(a) # s
    return lrModel(s)

def uctSearch(time_limit):
    """
    Variables:

    """
    while time_limit > time:
        pass

def backup(node, delta):
    """
    Variables:
    v, delta, N(v), Q(v)
    """
    while node is not None:
        node.visit_count += 1 # N(v)
        node.total_sim_reward += delta # Q(v)
        delta -= delta  # delta  -niet zeker of deze line klopt
        node = node.parent # v
