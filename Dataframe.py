import csv
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV


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
    # print(list(result.columns))
    return result

def findBestModel(log_model, x_data, y_data, x_test, y_test):
    """
    Zoekt beste parameters voor logistische regressie model.
    Duurt lang!
    """
    param_grid = [
        {'penalty' : ['l1', 'l2', 'elasticnet', 'none'],
        'solver' : ['lbfgs', 'newton-cg', 'liblinear', 'sag', 'saga'],
        'max_iter' : [100, 1000, 2500, 5000]
        }
    ]

    clf = GridSearchCV(log_model, param_grid=param_grid, cv=3, verbose=True, n_jobs=-1)

    best_clf = clf.fit(x_data, y_data)

    print(best_clf.best_estimator_)
    print(f'score: {best_clf.score(x_test, y_test)}')


def getModel(filename):
    """
    Traint een logistisch regressie model en slaat dat model op.
    """
    gameData = getDummies(filename)
    X = gameData.drop("result_Victory", axis=1)
    y = gameData["result_Victory"]
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    model = LogisticRegression(max_iter=1000, penalty='l1', solver='saga')

    # findBestModel(model, X_train, y_train, X_test, y_test)

    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))

    saveFileName = "lr_model_4_optimal.pkl"
    with open(saveFileName, 'wb') as file:
        pickle.dump(model, file)


getModel("gamesCombined-CLEANv3")