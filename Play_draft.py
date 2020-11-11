import MonteCarlo
from MonteCarlo import stateToVector
import pickle
import numpy as np
from Champions.champions import champion_names
from copy import deepcopy

TIME_LIMIT = 30     # tijd dat MCTS krijgt om de beste champion te zoeken
model = pickle.load(open('models/lr_model_5.pkl', 'rb'))

champion_dict = champion_names()
champion_dict_index = champion_dict[0]  # key = index           value = champion name
champion_dict_names = champion_dict[1]  # key = champion name   value = index
# print(champion_dict_index)

def championReccomender(x_node, dont_reccomend):
    """
    Deze functie gebruikt het MCTS algoritme om een champion aan te raden aan de speler.
    """
    recc_champion = MonteCarlo.uctSearch(4, x_node)
    recc_champion = recc_champion.state.blue_champions
    recc_champion = list(set(recc_champion).difference(dont_reccomend))
    print(f'MCTS raadt aan om {champion_dict_index[recc_champion[0]]} te kiezen.')

def Drafter():
    """
    Start een game en speel tegen een bot.
    """

    node = MonteCarlo.Mcts(MonteCarlo.Draft()) # set initial node (root)
    dont_recc = set()

    while node.state.terminal_state() is False:

        set_blue_champs = set()

        # node_copy = deepcopy(node) 
        # championReccomender(node_copy, dont_recc)

        while True:

            while True:     # in deze while-loop kiest de speler een champion d.m.v. champion naam
                try:
                    pick_blue = input('Kies een champion: ')
                    pick_blue_index = champion_dict_names[pick_blue.lower()] # haal de index van gekozen champion op
                    dont_recc.add(pick_blue_index)
                    break
                except KeyError:
                    print('Deze champion bestaat niet.')

            if (pick_blue_index in node.state.blue_champions) or (pick_blue_index in node.state.red_champions):     # check of champion al gekozen in.
                print('Deze champion is al gekozen.')
                continue      
            else:
                break
        
        
        set_blue_champs.add(pick_blue_index) 
        node = MonteCarlo.Mcts(node.state.get_next_state(set_blue_champs))      # update game-state met champion pick door speler
        
        pick_red = MonteCarlo.uctSearch(20, node)    # Run MCTS om een champion te krijgen voor red-side
        now_state = (pick_red.state.blue_champions, pick_red.state.red_champions )
        node = MonteCarlo.Mcts(node.state.get_next_state(now_state[1]))     # update game-state met champion pick door MCTS

        print(f'Blue side: {[champion_dict_index[i] for i in node.state.blue_champions]} \nRed side: {[champion_dict_index[i] for i in node.state.red_champions]}')

    # b_champs_to_name = [champion_dict_index[i] for i in node.state.blue_champions]
    # r_champs_to_name = [champion_dict_index[i] for i in node.state.red_champions]

    # print(f'Bue side: {b_champs_to_name} \nRed side: {r_champs_to_name}')
    combined = stateToVector(node.state)
    predicted_wr = model.predict_proba([combined])  # geeft voorspelling over wie game gaat winnen met LR-model die ook gebruikt wordt in MCTS

    print(f'De kans dat Blue wint met dit team is {round(100 * predicted_wr[0][1], 2)}%. \nDe kans dat Red wint is {round(100 * predicted_wr[0][0], 2)}%.')

Drafter()