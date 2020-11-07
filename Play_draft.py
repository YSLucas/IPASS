import MonteCarlo
import pickle
import numpy as np
import itertools
from Champions.champions import champion_names

TIME_LIMIT = 45
model = pickle.load(open('models/lr_model_1.pkl', 'rb'))

champion_name_dict = champion_names()

# model test

# blue_vector = [0] * 150
# red_vector = [0] * 150
# b_c = [0, 4, 2, 7, 3]
# r_c = [66, 44, 88, 101, 111]
# for hero_blue in b_c:
#     blue_vector[hero_blue] = 1
# for hero_red in r_c:
#     red_vector[hero_red] = 1
# combined = blue_vector + red_vector
# print(model.predict_proba([combined])) # laat % kans zien van de voorspelling. [0.22, 0,78] = 22% kans op 0, 78% kans op 1
# print(model.predict([combined])) # 1 is blue win in dit geval

# champions = set(range(1, 20)) # 150 champions * 2
# blue_champions = set()
# red_champions = set()
# remaining_champions = champions
# actionList = []
# actions = itertools.permutations(remaining_champions, (4))
# for a in actions:
#     actionList.append(a)
# print(actionList[1])


def Drafter():

    node = MonteCarlo.Mcts(MonteCarlo.Draft())

    blue_turn = True

    while node.state.terminal_state() is False:
        # choices = node.state.get_actions()
	    # choices_sets = [set(i) for i in choices]

        move = node.state.move_count # number of which move were on
        set_blue_champs = set()

        while True:
            pick_blue = int(input('Kies een Champion (getal tussen 1 en 150)'))
            if (pick_blue in node.state.blue_champions) or (pick_blue in node.state.red_champions):
                print('Deze champion is al gekozen')
                continue
            elif (pick_blue > 149) or (pick_blue < 0):
                print('Deze champion bestaat niet')
                continue        
            else:
                break
        
        
        set_blue_champs.add(pick_blue)
        print(set_blue_champs)
        print(type(set_blue_champs))
        node = MonteCarlo.Mcts(node.state.get_next_state(set_blue_champs))
        
        res = MonteCarlo.uctSearch(140, node)
        see = (res.state.blue_champions, res.state.red_champions )
        node = MonteCarlo.Mcts(node.state.get_next_state(see[1]))

        print(f'Bue side: {node.state.blue_champions} \nRed side: {node.state.red_champions}')

    b_champs_to_name = [champion_name_dict[i] for i in node.state.blue_champions]
    r_champs_to_name = [champion_name_dict[i] for i in node.state.red_champions]

    print(f'Bue side: {b_champs_to_name} \nRed side: {r_champs_to_name}')

Drafter()