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

HOST = "https://www.hltv.org"


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


def getAllMatches(URL):
    """
    get all links and stars for every match and seve in "allMatchLinks.pickle"
    :param URL: url to match-list page
    :return: nothing
    """
    allMatchLinks = []
    for i in range(1, 200):
        tmpUrl = URL + str(100 * i)  # gen URL for every page with matches
        html = requests.get(tmpUrl)
        soup = BeautifulSoup(html.content, 'html.parser')

        items = soup.find_all('div', {"class": "result-con"})  # find all matches on page
        for item in items:
            link = item.find('a').get('href')  # get link for every match
            stars = item.find_all('i', {"class": "fa fa-star star"})  # get stars for every match
            allMatchLinks.append([f"{HOST}{link}", len(stars)])  # add this info to list

        # print info and pause
        sys.stdout.write("\r{0}".format(f'{i}/200'))
        time.sleep(0.5)

    with open('allMatchLinks.pickle', 'wb') as f:
        pickle.dump(allMatchLinks, f)
    print('done')


def getMatchInfo():
    """
    get all stats for every match from "allMatchLinks.pickle"
    it gets [link, date, stars, res(dict), team1, team2, player11-player25(list)]
    save into "allMatchesInfo.pickle"
    :return: nothing
    """
    allMatchLinks = getPickleData('allMatchLinks.pickle')
    lines = []

    # for i in range(0, 10):
    # for i in range(0, len(allMatchLinks)):
    i = 10100
    while i < len(allMatchLinks):
        soup = None
        try:
            html = requests.get(allMatchLinks[i][0])  # get html page
            soup = BeautifulSoup(html.content, 'html.parser')  # get soup page

            # find teams and date
            team1 = HOST + soup.find('div', {"class": "team1-gradient"}).find('a').get('href')
            team2 = HOST + soup.find('div', {"class": "team2-gradient"}).find('a').get('href')
            date = soup.find('div', {"class": "date"}).get('data-unix')

            # try, cause some matches are didn't play (ex map: Default, score 1-0)
            try:
                # find all players
                players = soup.find('div', {'class': 'lineups'}).find_all('td', {"class": 'player'})
                for j in range(len(players)):
                    players[j] = HOST + str(players[j].find('a').get('href'))
                players = list(OrderedDict.fromkeys(players))  # soup find all players twice, and I made a set

                # find all played maps
                maps = {}
                iteamMaps = soup.find_all('div', {'class': 'played'})
                for j in range(0, len(iteamMaps), 2):
                    map = iteamMaps[j].find('div', {'class': 'mapname'}).get_text()  # get map name
                    res = iteamMaps[j].find_parent('div').find_all('div', {'class': 'results-team-score'})  # get score
                    res = f'{res[0].get_text()} {res[1].get_text()}'
                    maps[map] = res  # create dict

                # get finally line with all info
                line = [allMatchLinks[i][0], str(date), str(allMatchLinks[i][1]), maps, team1, team2, players]
                lines.append(line)
            except:
                pass

            # print info and pause
            sys.stdout.write("\r{0}".format(f'{i}/{len(allMatchLinks)}'))
            time.sleep(0.5)

        except Exception as e:
            print(e)
            if soup is not None:
                addToFile(os.path.join('Logs', f'{i}.html', soup.prettify()), 'w')  # save page
        finally:
            i += 1
        if (i + 1) % 100 == 0:
            # link, date, stars, res, team1, team2, p11-p25
            with open(os.path.join('MatchData', f'allMatchesInfo-{i + 1}.pickle'), 'wb') as f:
                pickle.dump(lines, f)
            lines = []


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


def getRang():
    pass


def getRangOld(URL):
    """

    :param URL: for team
    :return: in future
    """
    html = requests.get(URL)
    soup = BeautifulSoup(html.content, 'html.parser')
    # addToFile('page.txt', soup.prettify(), 'w') # save page

    item = soup.find('div', {"class": "graph"})  # find the graph
    graph = json.loads(item.get('data-fusionchart-config'))  # convert to json
    dataset = graph['dataSource']['dataset'][0]['data']  # leaves only the necessary information
    # for i in dataset:
    #     print(i)


def getPlayersStat():
    data = getPickleData("tempData.pkl")
    data = data.to_numpy()[:3:]

    dataWithPlayersStats = pd.DataFrame(data=None, index=None, columns=constants.columnsPlayersStatExcel)

    for match in range(len(data)):
        # try:
        maps = data[match][3:12:2]
        score = data[match][4:13:2]
        players = data[match][15:25]

        playersData = []
        # if teams played with full line-up
        if len(players) == 10:
            # go through each map
            for currMap in range(len(maps)):
                # if map is normal (not like TBD or default)
                if maps[currMap] in constants.MAPS_DICT:
                    print(maps[currMap])
                    # get current score for map
                    currScore = list(map(int, score[currMap].split(' ')))
                    # if map ended
                    if sum(currScore) >= 16:
                        playersData.append(playerPage(players, data[1], maps[currMap]))

            # if match was played it get all stat from past 3 month
            if len(playersData) != 0:
                playersData = playerPage(players, data[1]) + playersData
                # score[map] =
        print(maps)
        print(score)
        print(players)
        print(playersData)
        print("-----------=================--------------")
        # except Exception as ex:
        #     print(ex)


def playerPage(players, matchDate, currMap=None):
    matchDate = getDate(matchDate) if currMap == None else f'{getDate(matchDate)}&maps={constants.HLTV_MAPS_DICT[currMap]}'
    players = list(map(str, players.split('/')))[-2:]
    players = players[0]+'/'+players[1]
    link = constants.PLAYERS_STAT+players+matchDate
    print(link)


def getDate(matchDate):
    start = int(matchDate) // 1000
    end = int(matchDate) // 1000 - (86400 * 90)

    start = time.strftime('%Y-%m-%d', time.localtime(start))
    end = time.strftime('%Y-%m-%d', time.localtime(end))
    line = f"?startDate={end}&endDate={start}"

    #print(line)
    return line


def test():
    data = getPickleData("tempData.pkl")
    data = list(data.to_numpy()[:3:])
    newdata = pd.DataFrame(data=None, index=None, columns=constants.columns)
    for i in range(len(data)):
        newdata.loc[i] = data[i]
    print(type(newdata))
    print(newdata)
    # data.to_excel('Test_table1.xlsx')


if __name__ == "__main__":
    np.set_printoptions(linewidth=3000)
    # getRang("https://www.hltv.org/team/10672/vertex")
    # getAllMatches("https://www.hltv.org/results?offset=")
    # getPickleData('allMatchLinks.pickle')
    # getMatchInfo()
    # connectData()
    # getPlayersStat()
    playerPage('https://www.hltv.org/player/20384/zannn','1650441600000', 'Overpass')
    # test()
    # getPickleData(os.path.join('MatchData',f'allMatchesInfo-10.pickle'), True)
