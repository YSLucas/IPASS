import random
from random import choice
import numpy as np
import time
import pickle

MODEL_PATH = 'models/lr_model_1.pkl'
model = pickle.load(open(MODEL_PATH, 'rb'))

"""
Dit algoritme is gemodelleerd naar de pseudocode van Monte Carlo Tree Search UCT (http://ccg.doc.gold.ac.uk/ccg_old/papers/browne_tciaig12_1.pdf, blz. 9).

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
        if self.terminal_state():
            return None
        if self.actions == None:
            pass
        return self.actions

    def get_next_state(self, action):
        state = Draft(not self.blue_moves_next, self.blue_champions, self.red_champions, self.move_count+1)
        if self.blue_moves_next:
            state.blue_champions = self.blue_champions.union(action)
        else:
            state.red_champions = self.red_champions.union(action)

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
    blue_vector = np.zeros((1, 150))
    red_vector = np.zeros((1, 150))
    for hero_blue in s.blue_champions:
        blue_vector[hero_blue] = 1
    for hero_red in s.red_champions:
        red_vector[hero_red] = 1
    combined = blue_vector + red_vector
    blue_win_rate = model(combined)



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

def defaultPolicy(s):
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
    timer = time.time()
    root = Mcts(None)
    while time_limit > (time.time() - timer):
        v1 = treePolicy(root) #root node
        delta = defaultPolicy(v1.state, model)
        backup(v1.state, delta)
    return bestChild(root, 0)
        

def backup(node, delta):
    """
    Variables:
    v, delta, N(v), Q(v)
    """
    while node is not None:
        node.visit_count += 1 # N(v)
        node.total_sim_reward += delta # Q(v)
        delta = 1 - delta  # delta  -niet zeker of deze line klopt
        node = node.parent # v
