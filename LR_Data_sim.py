import csv
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def csvData():
    with open('2020 spring match data OraclesElixir 2020-05-15 (1).csv', 'r') as file:
        reader = csv.reader(file)
        data =  list(reader)
        dataDict = {}
        for row in data:
            if row[0] in dataDict:
                if row[12] == '':
                    continue
                else:
                    dataDict[row[0]].append(row[12])
            else:
                if row[12] == '':
                    dataDict[row[0]] = []
                else:
                    dataDict[row[0]] = [row[12]]
    return dataDict


def csvCutter():
    f=pd.read_csv("2020 spring match data OraclesElixir 2020-05-15 (1) - kopie.csv")
    keep_col = ['gameid','champion','result']
    new_f = f[keep_col]
    new_f.to_csv("testttt.csv", index=False)

def csvModify():
    df = pd.read_csv("testttt.csv")
    df['group_num'] = df.groupby('gameid')['champion'].transform(lambda x: range(1, len(x)+1))

    # df.pivot(index='gameid', columns='group_num')
    print(df.sample(3))
    df = df.pivot(index='gameid', columns='group_num')
    print(df.sample(3))
    # df.columns = [''.join([lvl1, str(lvl2)]) for lvl1, lvl2 in df.columns]
    # print(df.sample(3))
    # dfMod = df.drop(columns=['champion11', 'champion12', 'result2', 'result3', 'result4', 'result5', 'result6', 'result7', 'result8', 'result9', 'result10', 'result11', 'result12'])
    # print(dfMod.sample(3))
    # dfMod = pd.get_dummies(dfMod, drop_first=True)
    # print(dfMod.sample(3))

def dict2Dataframe(data):
    df = pd.DataFrame.from_dict(data, orient='index')
    df = pd.get_dummies(df, drop_first=True, columns=[''])
    print(df.sample(3))

# csvModify()

# with open('testttt.csv', 'r') as file:
#         reader = csv.reader(file)
#         data =  list(reader)
#         dataDict = []
#         for row in data:
#             if row[1] in dataDict:
#                 continue
#             else:
#                 dataDict.append(row[1])
#         print(len(dataDict))

def getDataFrame():
    """
        Maakt een vector die kan worden gebruikt voor logistische regressie
    """
    #   Maakt een dataframe van .csv met data
    df = pd.read_csv('gamesBrServer.csv')

    #   Zet 'result'-kolom om in dummies, en dropt onnodige kolommen
    dummie = pd.get_dummies(df, columns=['result'], drop_first=True)
    dummie = dummie.drop(['server', 'mmr', 'timestamp', 'team_1', 'team_2'], axis='columns')
    print(dummie.sample(10))

    #   Deze code zorgt ervoor dat de LoL-karakters later op de juiste ingedeeld kunnen worden
    dummieTeam1 = df['team_1'].str.get_dummies(sep=',')
    dummieTeam2 = df['team_2'].str.get_dummies(sep=',')

    #   Voegt de dummies van result, team_1 en team_2 samen
    mergedDummies = pd.concat([dummieTeam1, dummieTeam2.reindex(dummieTeam1.index)], axis=1)
    result = pd.concat([mergedDummies, dummie], axis=1)
    # print(dummieTeam1.sample(5))
    # print(dummieTeam2.sample(5))
    print(result.sample(5))

# pd.set_option('display.max_columns', None)
getDataFrame()