import pickle

import os
import sys

import pandas as pd
import numpy as np

import constants


def addToFile(file, line, format='a'):
    file = open(file, format, encoding="utf-8")
    file.write(str(line) + "\n")
    file.close()


def getPickleData(name, prnt=False):
    """

    :param name: name of file
    :param prnt: print?
    :return: information from pickle file
    """
    with open(name, 'rb') as f:  # open pickle file
        data_new = pickle.load(f)

    # print if it needs
    if prnt:
        print(len(data_new))
        for i in data_new:
            print(i)

    return data_new


def connectData():
    """
    get all data from pickles files into one
    :return:
    """
    allData = []

    # get all data from pickles files
    for i in range(1, 200):
        name = os.path.join('MatchData', f'allMatchesInfo-{i * 100}.pickle')
        newData = getPickleData(name)
        allData += newData
        sys.stdout.write("\r{0}".format(f'{i}/199'))
    print('\n all info collected')

    # convert info to np array
    dadaArray = np.array(allData)

    # convert maps and players list into one list
    mapsScore = []
    players = []
    for i in range(len(dadaArray)):
        mapsList = list(dadaArray[i][3])  # temp maps from one match
        scoreList = [dadaArray[i][3][x] for x in mapsList]  # temp score from one match
        for j in range(5):
            try:
                mapsScore.append(mapsList[j])  # add maps into new list
                mapsScore.append(scoreList[j])  # add score into new list
            except:
                mapsScore.append(None)  # if maps ended it add None to list
                mapsScore.append(None)  # if score ended it add None to list
        if len(dadaArray[i][6]) == 10:
            players += dadaArray[i][6]
        else:
            line = dadaArray[i][6]
            # print(len(line), 10-len(line))
            for j in range(10 - len(line)):
                line.append(None)
            players += line
        sys.stdout.write("\r{0}".format(f'{i}/{len(dadaArray)}'))
    print('\n edit maps and players lists')

    # add all data to new array
    editAllData = np.zeros((len(dadaArray), 25), dtype=object)  # initialize new array
    for i in range(len(editAllData)):
        # the first 3 remain in place(link to match, time, stars)
        (editAllData[i][0], editAllData[i][1], editAllData[i][2]) = (dadaArray[i][0], dadaArray[i][1], dadaArray[i][2])

        # next 10 fields it's a map score
        for j in range(10):
            editAllData[i][j + 3] = mapsScore[i * 10 + j]

        # next 2 it's teams links
        (editAllData[i][13], editAllData[i][14]) = (dadaArray[i][4], dadaArray[i][5])

        # last 10 fields its players
        for j in range(10):
            editAllData[i][j + 15] = players[i * 10 + j]

        sys.stdout.write("\r{0}".format(f'{i}/{len(editAllData)}'))
    print('\n Saving into excel')

    # create excel table
    allItemsPD = pd.DataFrame(editAllData, columns=constants.columns, index=None)
    # allItemsPD.to_excel('Test_table.xlsx')
    print('\n Saving into pickle file')
    allItemsPD.to_pickle("tempData.pkl")
    print('\n done')


def converToExcel():
    data = []
    for i in range(10,41):
        try:
            data += getPickleData(os.path.join('PlayersStats', f'PlayersStats-{i}.pickle'))
        except:
            pass
    dataWithPlayersStats = pd.DataFrame(data=data, index=None, columns=constants.columnsPlayersStatExcel)
    dataWithPlayersStats.to_excel('Test_table_players_stats.xlsx')


if __name__ == "__main__":
    converToExcel()
