import pandas as pd
import pickle
import os

print(os.getcwd())

def champion_names():

    champion_list = []
    with open ('Champions/champions_list', 'rb') as fp:
        champion_list = pickle.load(fp)

    champion_list = list(dict.fromkeys(champion_list)) # remove dupes
    champion_list.pop()

    champion_dict = {}
    counter = 0
    for champion in champion_list:
        champion_dict[counter] = champion
        counter += 1

    return champion_dict