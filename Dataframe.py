import csv
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def getDummies():
    """
        Maakt een vector die kan worden gebruikt voor logistische regressie
    """
    #   Maakt een dataframe van .csv met data
    df = pd.read_csv('games-NoDupes.csv')

    #   Zet 'result'-kolom om in dummies, en dropt onnodige kolommen
    dummie = pd.get_dummies(df, columns=['result'], drop_first=True)
    dummie = dummie.drop(['server', 'mmr', 'timestamp', 'team_1', 'team_2'], axis='columns')

    #   Deze code zorgt ervoor dat de LoL-karakters later op de juiste ingedeeld kunnen worden
    dummieTeam1 = df['team_1'].str.get_dummies(sep=',')
    dummieTeam2 = df['team_2'].str.get_dummies(sep=',')

    #   Voegt de dummies van result, team_1 en team_2 samen
    mergedDummies = pd.concat([dummieTeam1, dummieTeam2.reindex(dummieTeam1.index)], axis=1)
    result = pd.concat([mergedDummies, dummie], axis=1)
    # print(dummieTeam1.sample(5))
    # print(dummieTeam2.sample(5))
    print(result.sample(5))

pd.set_option('display.max_columns', None)
getDummies()