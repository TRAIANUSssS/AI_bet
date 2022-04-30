import json
import pickle
import time

import os
import sys

from collections import OrderedDict
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

import constants
import PickleFiles
import Date


def getPlayersStat():
    data = PickleFiles.getPickleData("tempData.pkl")
    data = data.to_numpy()[:101:]

    dataWithPlayersStats = []  # pd.DataFrame(data=None, index=None, columns=constants.columnsPlayersStatExcel)

    iteration = 0
    allMapsCount = getAllMapCount(data)
    delay = datetime.now()
    allTime = datetime.now()
    for match in range(iteration, len(data)):
        sys.stdout.write(
            "\r{0}".format(f'{iteration}/{allMapsCount}, {datetime.now() - delay}, {datetime.now() - allTime}'))
        delay = datetime.now()
        # for match in range(0):
        try:
            maps = data[match][3:12:2]
            score = data[match][4:13:2]
            winner = []
            players = data[match][15:25]

            playersData = []
            playersLinks = []

            if len(players) == 10:  # if teams played with full line-up
                mapCount = 5 - ((maps == None).sum())  # how many maps was played
                for currMap in range(len(maps)):  # go through each map
                    if maps[currMap] in constants.MAPS_DICT:  # if map is normal (not like TBD or default)
                        # print(maps[currMap])
                        currScore = list(map(int, score[currMap].split(' ')))  # get current score for map
                        winner.append(0 if currScore[0] < currScore[1] else 1)
                        if sum(currScore) >= 16:  # if map ended
                            # get links to players profile with time and map
                            playersLinks += (playerProfileLink(players, data[match][1], maps[currMap]))

                # if match was played it get links to players profile with time and without map
                if len(playersLinks) != 0:
                    playersLinks = playerProfileLink(players, data[match][1]) + playersLinks

                playersData = getPlayerProfileStat(playersLinks, mapCount)
                allTimeStat = playersData[:80]
                for currMap in range(1, mapCount + 1):
                    mapStat = playersData[80 + 70 * (currMap - 1):80 + 70 * currMap]
                    normalList = []
                    for i in range(10):
                        normalList += allTimeStat[i * 8:(i + 1) * 8] + mapStat[i * 7:(i + 1) * 7]
                    dataFrameWithPlayersStats = data[match][:3].tolist() + \
                                                [maps[currMap - 1], score[currMap - 1], winner[currMap - 1], currMap] + \
                                                data[match][13:15].tolist() + \
                                                normalList
                    dataWithPlayersStats.append(dataFrameWithPlayersStats)
                    iteration += 1
                    if (iteration + 1) % 10 == 0:
                        with open(os.path.join('PlayersStats', f'PlayersStats-{iteration + 1}.pickle'), 'wb') as f:
                            pickle.dump(dataWithPlayersStats, f)
                            dataWithPlayersStats = []
                    # print(len(dataFrameWithPlayersStats))

            # print(maps)
            # print(score)
            # print(players)
            # print(playersLinks)
            # print(playersData)
            # print(playersData[:80], playersData[80:80 + 70], playersData[80 + 70:80 + 70 * 2])
            # print("-----------=================--------------")
        except Exception as ex:
            print(ex)
            maps = data[match][3:12:2]
            for currMap in maps:
                if currMap in constants.MAPS_DICT:
                    iteration += 1
    with open(os.path.join('PlayersStats', f'PlayersStats-{iteration + 1}.pickle'), 'wb') as f:
        pickle.dump(dataWithPlayersStats, f)


def playerProfileLink(players, matchDate, currMap=None):
    matchDate = Date.getDate(
        matchDate) if currMap == None else f'{Date.getDate(matchDate)}&maps={constants.HLTV_MAPS_DICT[currMap]}'
    playersStats = []
    for player in players:
        playerLink = list(map(str, player.split('/')))[-2:]
        playerLink = playerLink[0] + '/' + playerLink[1]
        link = constants.PLAYERS_STAT + playerLink + matchDate
        playersStats.append(link)
        # print(link)
    return playersStats


def getPlayerProfileStat(playersLinks, mapCount):
    stat = []
    for j in range(mapCount + 1):
        for i in range(10):
            html = requests.get(playersLinks[i + (j * 10)])  # get html page
            soup = BeautifulSoup(html.content, 'html.parser')  # get soup page

            nickname = soup.find('h1', {'class': 'summaryNickname text-ellipsis'}).text
            rating = soup.find('span', {'class': 'strong'}).text
            items = soup.find_all('div', {'class': 'stats-row'})
            kd = items[3].find_all('span')[1].text
            dpr = items[4].find_all('span')[1].text
            kpr = items[8].find_all('span')[1].text
            apr = items[9].find_all('span')[1].text
            depr = items[10].find_all('span')[1].text
            line = [playersLinks[i + (j * 10)], rating, kd, dpr, kpr, apr, depr]
            if j == 0:
                stat.append(nickname)
            stat += line
            time.sleep(0.5)
    return stat


def getAllMapCount(data):
    allPossipelMapCount = []
    for i in range(3, 12, 2):
        allPossipelMapCount += data[:, i].tolist()
    # print(len(allPossipelMapCount) - allPossipelMapCount.count(None))
    count = 0
    for i in constants.MAPS_DICT:
        count += allPossipelMapCount.count(i)
    return count


def converToExcel():
    data = PickleFiles.getPickleData(os.path.join('PlayersStats', 'PlayersStats-5.pickle'))
    dataWithPlayersStats = pd.DataFrame(data=data, index=None, columns=constants.columnsPlayersStatExcel)
    dataWithPlayersStats.to_excel('Test_table_players_stats.xlsx')
