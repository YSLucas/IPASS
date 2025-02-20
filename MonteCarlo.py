import random
from random import choice
import numpy as np
import time
import pickle
import itertools
from copy import deepcopy
import math

MODEL_PATH = 'models/lr_model_5.pkl'
# EXPLORATION_C = (2**-3)
EXPLORATION_C = 1 / np.sqrt(2)
# EXPLORATION_C = 2
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
    
    def __init__(self, blue_move=True, blue_champions=set(), red_champions=set()):
        self.blue_move = blue_move
        self.blue_champions = blue_champions # list van champion id's [2, 33, 45] = champion 2; 33 en 45
        self.red_champions = red_champions # list van champion id's, ook van 1 tm 150; zodat get_actions beter werkt.
        self.actions = None
    
    def check_blue_move(self):
        return self.blue_move

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
        Maakrt volgende game-state aan de hand vorige game-state en actie die wordt genomen.
        """
        state = Draft(not self.blue_move, self.blue_champions, self.red_champions)
        if self.blue_move:
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
        self.remaining_actions = deepcopy(self.state.get_actions())

    def expand(self):
	    action = random.choice(self.remaining_actions)
	    self.remaining_actions.remove(action)
	    child = Mcts(self.state.get_next_state(action), action, self)
	    self.children.append(child)
	    return child


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

    # onderstaande snippet is om predict_proba te gebruiken om rewards uit te rekenen.
    # ik heb deze versie gemaakt zodat kleine wins (bijv. 51% kans) niet evenzwaar meetellen als 70% kans wins

    blue_win_rate = model.predict_proba([vector])[0]
    if s.blue_move:
        if blue_win_rate[1] > blue_win_rate[0]: # [1] is % kans uitkomst is 1, [0] % kans op 0
            return (blue_win_rate[1], 0)  # (reward van kant die algoritme uitvoert, reward tegenstander)
        else:
            return (0, blue_win_rate[0])
    else:
        if blue_win_rate[1] > blue_win_rate[0]:
            return (0, blue_win_rate[1]) 
        else:
            return (blue_win_rate[0], 0)

    # onderstaande snippet is de originele code om rewards uit te rekenen    

    # blue_win_rate = model.predict([vector])
    # if side == 'blue':
    #     if blue_win_rate == 0:
    #         return blue_win_rate
    #     else:
    #         return blue_win_rate
    # else:
    #     if blue_win_rate == 1:  # als MCTS door red-side wordt uitgevoerd zijn de rewards omgedraaid (blue_win_rate == 1 is een verlies, 0, voor red)
    #         return 0
    #     else:
    #         return 1

# def expand(node):
#     """
#     expand genereert child nodes voor een node.

#     Variables:
#     v, v', a, s, 
#     """
#     action = random.choice(node.remaining_actions)
#     node.remaining_actions.remove(action)
#     child = Mcts(node.state.get_next_state(action), action, node)
#     node.children.append(child)
#     return child # v'
 
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
                                + (c) * np.sqrt( (np.log(node.visit_count) )/ x.visit_count))  # exploration
    return maxC

def mostVisited(node):
    """
    i.p.v. best child te bepalen door de formule nog een keer te gebruiken kan je ook de meest bezochte node geven als beste volgende actie.
    Het verschil tussen deze manier and bestChild() manier is niet groot. 
    (source: http://ccg.doc.gold.ac.uk/ccg_old/papers/browne_tciaig12_1.pdf)
    """
    child = node.children
    mostV = max(child, key=lambda x: x.total_sim_reward)
    print(f'Visit count: {mostV.visit_count}. Total reward: {mostV.total_sim_reward}')
    return mostV

def treePolicy(node):
    """
    treePolicy selecteert of maakt een node vanaf een gegeven al bestaande node.

    Variables:
    v, c
    """
    while node.state.terminal_state() is False:
        if len(node.remaining_actions) != 0:
            return node.expand() # maakt een child van node met random action
            # return expand(node)
        else:
            node = bestChild(node, EXPLORATION_C) # geeft beste child van node
            # node_v = bestChild(node, c)
    return node

def defaultPolicy(s):
    """
    Simuleert een gegeven node tot een terminal state en geeft een reward van de terminal state

    Variables:
    s, a
    """
    # b_r = not s.blue_move
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
    blue = 0
    red = 0
    while time.time() < (budget + timer_start):
        v1 = treePolicy(root_node)      # return best child
        delta = defaultPolicy(v1.state)     # geeft reward van bestChild van node v1
        backup(v1, delta)   # gaat terug in de boom om nodes te updaten
        depth += 1
        # time.sleep(0.001)
        if v1.state.blue_move:
            blue += 1
        else:
            red += 1
    print(f'blue {blue}: red {red}')
    print(f'Iterations: {depth}')

    # return bestChild(root_node, 0)   # return bestChild van root 
    return mostVisited(root_node)      # bestChild gebaseerd op meest bezochte node
    
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
    delta_copy = delta
    index_delta = 0
    delta = delta[0]
    while node != None:
        node.visit_count += 1 # N(v)
        # node.total_sim_reward += delta # Q(v)
        node.total_sim_reward = node.total_sim_reward + delta  # Q(v)
        # if delta == 1:
        #     delta = 0
        # elif delta == 0:
        #     delta = 1
        index_delta = 1 - index_delta
        delta = delta_copy[index_delta]

        node = node.parent # v
