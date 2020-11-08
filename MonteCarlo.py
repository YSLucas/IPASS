import random
from random import choice
import numpy as np
import time
import pickle
import itertools
from copy import copy
import math

MODEL_PATH = 'models/lr_model_1.pkl'
EXPLORATION_C = (2**-6)
# EXPLORATION_C = 1 / np.sqrt(2)
model = pickle.load(open(MODEL_PATH, 'rb'))
champions = set(range(0, 150)) # 150 champions

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
△(delta) = reward
"""

class Draft:
    
    def __init__(self, blue_moves_next=True, blue_champions=set(), red_champions=set()):
        self.blue_moves_next = blue_moves_next
        self.blue_champions = blue_champions # list van champion id's [2, 33, 45] = champion 2; 33 en 45
        self.red_champions = red_champions # list van champion id's, ook van 1 tm 150; zodat get_actions beter werkt.
        self.actions = None

    def terminal_state(self):
        """
        Check of een game over is. Bij 10 gekozen champions (5 blue + 5 red) is een game over.
        """
        if len(self.blue_champions) == 5 and len(self.red_champions) == 5: 
            return True
        else:
            return False

    def get_actions(self):
        """
        Zoekt naar alle champions die nog niet zijn gekozen in betreffende game.
        """
        if self.terminal_state():
            return []
        if self.actions == None:
            remaining_champions = champions.difference(self.blue_champions.union(self.red_champions)) # blue = [1, 6, 55] & red = [33, 7, 3] -> remaining_champions = [all champions] - [1, 3, 6, 7, 33, 55]
            picks = 1
            self.actions = list(itertools.combinations(remaining_champions, (picks)))   # picks geef aan hoeveel champions er in deze ronde worden gekozen
        return self.actions

    def get_next_state(self, action):
        """
        Maakr volgende game-state aan de hand vorige game-state en actie die wordt genomen.
        """
        state = Draft(not self.blue_moves_next, self.blue_champions, self.red_champions)
        if self.blue_moves_next:
            # print(action)
            state.blue_champions = self.blue_champions.union(action) # de gekozen action (een champion) wordt uitgevoerd en aan blue_champions toegevoegd
        else:
            # print(action)
            state.red_champions = self.red_champions.union(action)
        return state

class Mcts:

    def __init__(self, state=Draft(), incoming_action=None, parent=None, total_sim_reward=0
                 , visit_count=0):
        self.state = state # s
        self.incoming_action = incoming_action
        self.parent = parent
        self.total_sim_reward = total_sim_reward # Q(v)
        self.visit_count = visit_count # N(v)
        self.children = []
        self.remaining_actions = copy(self.state.get_actions())

def stateToVector(s):
    """
    Zet een terminal-state om in een vector die gebruikt kan worden door het LR model om een voorspelling te geven.
    """
    
    blue_vector = [0] * 150
    red_vector = [0] * 150
    for hero_blue in s.blue_champions:
        blue_vector[int(hero_blue)] = 1 # zet 1-en neer bij de indexen van de champions in de random gekozen state voor blue side
    for hero_red in s.red_champions:
        red_vector[int(hero_red)] = 1
    combined = blue_vector + red_vector
    return combined

def lrModel(s):
    """
    Hier wordt de reward voor red-side uitgerekend met het LR model.
    """
    vector = stateToVector(s)
    blue_win_rate = model.predict([vector]) #probeer dit ook nog met predict_proba te doen, misschien werkt reward fan beter
    if blue_win_rate == 1:
        return 0
    else:
        return 1
    
    # blue_win_rate = model.predict_proba([vector])[0][0]
    # return blue_win_rate

def expand(node):
    """
    expand genereert child nodes voor een node.

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
    
    Psuedocode bestChild:
    max(   
            ( Q(v') / N(v') ) +  c *  sqrt( ( 2ln N(v) ) / N(v') ) 
        )
    """
    child = node.children
    maxC = max(child, key=lambda x: 
                                (x.total_sim_reward / x.visit_count)      # exploitation
                                + c * math.sqrt( ( 2 * np.log(node.visit_count) )/ x.visit_count))  # exploration
    return maxC

def treePolicy(node):
    """
    treePolicy 

    Variables:
    v, c
    """
    while node.state.terminal_state() is False:
        if len(node.remaining_actions) != 0:
            # return node.expand() # maakt een child van node met random action
            return expand(node)
        else:
            node = bestChild(node, EXPLORATION_C) # geeft beste child van node
            # node_v = bestChild(node, c)
    return node

def defaultPolicy(s):
    """
    defaultPolicy kiest een random terminal state en geeft een reward terug met het LR model.

    Variables:
    s, a
    """
    while s.terminal_state() is False:
        pre = s.get_actions() # verzamel actions van state s
        a = random.choice(pre) # kies random action 
        s = s.get_next_state(a) # krijg volgende state
    return lrModel(s) # bereken reward van state s

def uctSearch(budget, root):
    """
    Vanaf deze functie wordt de UCT search uitgevoerd.

    Variables:
    v0, v1, △
    """
    timer_start = time.time()
    depth = 0
    root_node = Mcts(root.state)  # root node

    while time.time() < (budget + timer_start):
        v1 = treePolicy(root_node)      # return best child
        delta = defaultPolicy(v1.state)     # geeft reward van bestChild van node v1
        backup(v1, delta)   # gaat terug in de boom om nodes te updaten
        depth += 1
        time.sleep(0.01)
    # print(depth)
    return bestChild(root_node, 0)   # return bestChild van root 
    
    # deze snippet kan gebruikt worden om te stoppen bij een maximaal aantal iterations ipv tijd.
    # while budget > depth:
    #     v1 = treePolicy(root_node) #return best child
    #     delta = defaultPolicy(v1.state) # geeft reward van bestChild van node v1
    #     backup(v1, delta) # gaat terug in de boom om nodes te updaten
    #     depth += 1
    # return bestChild(root_node, 0) #return bestChild van root     

def backup(node, delta):
    """
    Gaat vanaf een end-node terug naar de root en update bij elke parent de visit_count en total_sim_reward.
    Variables:
    v, △, N(v), Q(v)
    """
    while node != None:
        node.visit_count += 1 # N(v)
        node.total_sim_reward += delta # Q(v)
        # delta = -1 * delta # reward
        node = node.parent # v
