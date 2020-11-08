import pandas as pd
import pickle
import os

print(os.getcwd())

def champion_names():
    """
    Maakt 2 dictionaries met champion namen en indexen op alfabetische volgorde.
    """
    champion_list = []
    with open ('Champions/champions_list', 'rb') as fp:
        champion_list = pickle.load(fp)

    champion_list = list(dict.fromkeys(champion_list)) # remove dupes
    champion_list.pop()

    champion_dict_index = {}
    champion_dict_names = {}
    counter = 0
    for champion in champion_list:
        champion_dict_index[counter] = champion
        counter += 1
    
    counter = 0
    for champion2 in champion_list:
        champion_dict_names[champion2.lower()] = counter
        counter += 1

    return (champion_dict_index, champion_dict_names)