import csv
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# pd.set_option('display.columns', None)

def getDummies(filename):
    """
    Maakt een vector die kan worden gebruikt voor logistische regressie
    """
    #   Maakt een dataframe van .csv met data
    df = pd.read_csv(filename + '.csv')

    #   Zet 'result'-kolom om in dummies, en dropt onnodige kolommen
    dummie = pd.get_dummies(df, columns=['result'], drop_first=True)
    dummie = dummie.drop(['server', 'mmr', 'timestamp', 'team_1', 'team_2'], axis='columns')

    #   Deze code zorgt ervoor dat de LoL-karakters later op de juiste ingedeeld kunnen worden
    dummieTeam1 = df['team_1'].str.get_dummies(sep=',')
    dummieTeam2 = df['team_2'].str.get_dummies(sep=',')

    #   Voegt de dummies van result, team_1 en team_2 samen
    mergedDummies = pd.concat([dummieTeam1, dummieTeam2.reindex(dummieTeam1.index)], axis=1)
    result = pd.concat([mergedDummies, dummie], axis=1)
    # print(dummieTeam1.iloc[1])
    # print(dummieTeam2.iloc[1])
    # print(result.sample(1))
    print(list(result.columns))
    return result


def getModel(filename):
    """
    Traint een logistisch regressie model en slaat dat model op.
    """
    gameData = getDummies(filename)
    X_train, X_test, y_train, y_test = train_test_split(gameData.drop("result_Victory", axis=1), gameData["result_Victory"])
    model = LogisticRegression()
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
    model

    saveFileName = "lr_model_1.pkl"
    with open(saveFileName, 'wb') as file:
        pickle.dump(model, file)


# getModel("gamesCombined-CLEANv3")
# gameData = getDummies("gamesCombined-CLEANv3")


# c_l = list(gameData.columns)
# with open('Champions/champions_list', 'wb') as fp:
#     pickle.dump(c_l, fp)

# X_train, X_test, y_train, y_test = train_test_split(gameData.drop("result_Victory", axis=1), gameData["result_Victory"])
# model = LogisticRegression()
# model.fit(X_train, y_train)
# print(model.score(X_test, y_test))
# print(np.zeros((1, 5)))
# print(set(range(0, 6)))

# print(set(range(1, 151)))
# model.predict()