import json
import pickle
import time
import traceback

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

errors, iteration, allMapsCount, matchNum, aLLMatchCount, delay, allTime, totalWaitsCount = (
    0, 0, 0, 0, 0, datetime.now(), datetime.now(), 0)


# 1814 edit except's
def getPlayersStat(matchStart, matchEnd):
    """
    get and save players stats into pickle file in format:
    ['link', 'date', 'stars', 'map', 'score', 'winner', 'mapNum', 'team1', 'team2',
    'nickname11', 'linkAllStat11',  'rating11', 'kd11', 'dpr11', 'kpr11', 'apr11', 'depr11',
                  'linkMapStat11', 'ratingMap11', 'kdMap11', 'dprMap11', 'kprMap11', 'aprMap11', 'deprMap11' ...]
    :param matchStart: start from point
    :param matchEnd: finish point
    :return: save info into pickle file
    """
    global errors, iteration, allMapsCount, matchNum, aLLMatchCount, delay, allTime

    data = PickleFiles.getPickleData("tempData.pkl")  # get all data
    prevData = data.to_numpy()[:matchStart:]  # get data from 0 to start point
    data = data.to_numpy()[matchStart:matchEnd:]  # get data from start to finish points
    # data = data.to_numpy()[268:269:]  # get data from start to finish points

    dataWithPlayersStats = []  # main list with complete players stat

    iteration = getAllMapCount(prevData)  # maps count from 0 to start point
    allMapsCount = getAllMapCount(data) + iteration  # all maps count
    aLLMatchCount = len(data) + len(prevData)
    matchNum = matchStart  # start parsing with
    print(
        f'Maps found: {allMapsCount} (start with {iteration}), Matches found: {aLLMatchCount} (start with {matchNum})')

    # get time for statistic
    delay = datetime.now()
    allTime = datetime.now()

    # print(data)  # """!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""

    # start parsing
    for match in range(len(data)):
        # print info
        printInfo()
        delay = datetime.now()

        # for match in range(0):
        try:
            maps = data[match][3:12:2]
            score = data[match][4:13:2]
            winner = []
            players = data[match][15:25]

            playersLinks = []  # rough stat

            if len(players) == 10:  # if teams played with full line-up
                mapCount = 5 - ((maps == None).sum())  # how many maps was played
                for currMap in range(len(maps)):  # go through each map
                    if maps[currMap] in constants.MAPS_DICT:  # if map is normal (not like TBD or default)
                        # print(maps[currMap])
                        try:
                            currScore = list(map(int, score[currMap].split(' ')))  # get current score for map
                            winner.append(0 if currScore[0] < currScore[1] else 1)
                            if sum(currScore) >= 16:  # if map ended
                                # get links to players profile with time and map
                                playersLinks += (playerProfileLink(players, data[match][1], maps[currMap]))
                        except:
                            winner.append(None)
                    else:
                        playersLinks += (playerProfileLink(None, data[match][1]))
                        winner.append(None)
                # print(winner)
                # print(mapCount)
                # if match was played it get links to players profile with time and without map
                if len(playersLinks) != 0:
                    # get links for all stat past 3 month
                    playersLinks = playerProfileLink(players, data[match][1]) + playersLinks

                    # parse all links
                    playersData = getPlayerProfileStat(playersLinks, mapCount)

                    # separate all stats from maps stats
                    allTimeStat = playersData[:80]

                    for currMap in range(1, mapCount + 1):  # went on every map
                        if maps[currMap - 1] in constants.MAPS_DICT:  # if map is need
                            # get stats from all maps into 2-d list
                            mapStat = playersData[80 + 70 * (currMap - 1):80 + 70 * currMap]
                            normalList = []  # list for write stat in normal form
                            for i in range(10):
                                normalList += allTimeStat[i * 8:(i + 1) * 8] + mapStat[i * 7:(i + 1) * 7]

                            # all what need for Excel table
                            dataFrameWithPlayersStats = data[match][:3].tolist() + \
                                                        [maps[currMap - 1],
                                                         score[currMap - 1],
                                                         winner[currMap - 1],
                                                         currMap] + \
                                                        data[match][13:15].tolist() + \
                                                        normalList
                            dataWithPlayersStats.append(dataFrameWithPlayersStats)

                            iteration += 1  # """!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
                            if (iteration + 1) % 10 == 0:  # every 10th iteration save data into file
                                with open(os.path.join('PlayersStats', f'PlayersStats-{iteration + 1}.pickle'),
                                          'wb') as f:
                                    pickle.dump(dataWithPlayersStats, f)
                                    dataWithPlayersStats = []

        except Exception as e:
            errors += 1
            # if error print name error, line, file, and line from data
            traceback.print_exc()
            print(f"DATA: {data[match]}")

            # add iteration index
            maps = data[match][3:12:2]
            for currMap in maps:
                if currMap in constants.MAPS_DICT:
                    iteration += 1
        finally:
            matchNum += 1
            # if iteration % 100 == 0:
            #     pass
            #     #time.sleep(180)
    # keep the rest of the information
    with open(os.path.join('PlayersStats', f'PlayersStats-{iteration + 1}.pickle'), 'wb') as f:
        pickle.dump(dataWithPlayersStats, f)


def playerProfileLink(players, matchDate, currMap=None):
    """
    receive links into players profile
    :param players:
    :param matchDate: time in mil secs from start epoch
    :param currMap: map for which need link (def val - link into profile without map)
    :return: list of links
    """
    # get date with or without map
    if players is not None:
        matchDate = Date.getDate(
            matchDate) if currMap == None else f'{Date.getDate(matchDate)}&maps={constants.HLTV_MAPS_DICT[currMap]}'
        playersStats = []
        for player in players:  # get index nd nickname for players
            playerLink = list(map(str, player.split('/')))[-2:]
            playerLink = playerLink[0] + '/' + playerLink[1]
            link = constants.PLAYERS_STAT + playerLink + matchDate
            playersStats.append(link)
        # print(link)
    else:
        playersStats = [None] * 10
    return playersStats


def getPlayerProfileStat(playersLinks, mapCount):
    """
    receive stats from players profile
    :param playersLinks: list with links into players profile
    :param mapCount: how many maps was played
    :return: 1-d list with stats
    """
    global errors, totalWaitsCount

    stat = []
    for j in range(mapCount + 1):
        for i in range(10):
            try:
                html = requests.get(playersLinks[i + (j * 10)])  # get html page
                while html.status_code != 200:
                    totalWaitsCount += 1
                    printInfo(30)
                    time.sleep(30)
                    html = requests.get(playersLinks[i + (j * 10)])  # get html page
                soup = BeautifulSoup(html.content, 'html.parser')  # get soup page

                # get all values
                nickname = soup.find('h1', {'class': 'summaryNickname text-ellipsis'}).text
                rating = soup.find('span', {'class': 'strong'}).text
                line = [playersLinks[i + (j * 10)], rating]

                items = soup.find_all('div', {'class': 'stats-row'})
                for k in [3, 4, 8, 9, 10]:
                    try:
                        line.append(items[k].find_all('span')[1].text)
                    except:
                        line.append(None)
                # kd = items[3].find_all('span')[1].text
                # dpr = items[4].find_all('span')[1].text
                # kpr = items[8].find_all('span')[1].text
                # apr = items[9].find_all('span')[1].text
                # depr = items[10].find_all('span')[1].text
                # line = [playersLinks[i + (j * 10)], rating, kd, dpr, kpr, apr, depr]

                if j == 0:
                    stat.append(nickname)
            except:
                errors += 1
                traceback.print_exc()
                print(f"DATA: {playersLinks[i + (j * 10)]}")
                try:
                    line = [playersLinks[i + (j * 10)], None, None, None, None, None, None]
                except:
                    line = [None, None, None, None, None, None, None]
            finally:
                stat += line
                time.sleep(0.75)
    return stat


def getAllMapCount(data):
    """

    :param data: sliced data list in witch we want received all maps which played
    :return: count of all played maps
    """
    allPossibleMapCount = []
    for i in range(3, 12, 2):
        allPossibleMapCount += data[:, i].tolist()
    count = 0
    for i in constants.MAPS_DICT:
        count += allPossibleMapCount.count(i)
    return count


def printInfo(someTime=0):
    sys.stdout.write(
        "\r{0}".format(
            f'Map: {iteration}/{allMapsCount}, '
            f'Match: {matchNum}/{aLLMatchCount}, '
            f'Prev iteration time {datetime.now() - delay}, '
            f'Total time {datetime.now() - allTime}, '
            f'Errors: {errors}, '
            f'Wait: {someTime}, '
            f'Total waits count: {totalWaitsCount}  '))
