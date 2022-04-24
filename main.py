import json
import pickle
import time
import os
import sys
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup

HOST = "https://www.hltv.org"


def addToFile(file, line, format='a'):
    file = open(file, format, encoding="utf-8")
    file.write(line + "\n")
    file.close()


def getMatchInfo():
    """
    get all stats for every match from "allMatchLinks.pickle"
    it gets [link, date, stars, res(dict), team1, team2, player11-player25(list)]
    save into "allMatchesInfo.pickle"
    :return: nothing
    """
    allMatchLinks = getPickleData('allMatchLinks.pickle')
    lines = []

    try:
        # for i in range(0, 10):
        for i in range(0, len(allMatchLinks)):
            html = requests.get(allMatchLinks[i][0])  # get html page
            soup = BeautifulSoup(html.content, 'html.parser')  # get soup page

            # find teams and date
            team1 = HOST + soup.find('div', {"class": "team1-gradient"}).find('a').get('href')
            team2 = HOST + soup.find('div', {"class": "team2-gradient"}).find('a').get('href')
            date = soup.find('div', {"class": "date"}).get('data-unix')

            # find all players
            players = soup.find('div', {'class': 'lineups'}).find_all('td', {"class": 'player'})
            for j in range(len(players)):
                players[j] = HOST + players[j].find('a').get('href')
            players = list(OrderedDict.fromkeys(players))  # soup find all players twice, and I made a set

            # find all played maps
            maps = {}
            iteamMaps = soup.find_all('div', {'class': 'played'})
            for j in range(0, len(iteamMaps), 2):
                map = iteamMaps[j].find('div', {'class': 'mapname'}).get_text()  # get map name
                res = iteamMaps[j].find_parent('div').find_all('div', {'class': 'results-team-score'})  # get score
                res = f'{res[0].get_text()} {res[1].get_text()}'
                maps[map] = res  # create dict

            # get finaly line with all info
            line = [allMatchLinks[i][0], str(date), str(allMatchLinks[i][1]), maps, team1, team2, players]
            lines.append(line)

            # print info and pause
            sys.stdout.write("\r{0}".format((f'{i}/{len(allMatchLinks)}')))
            time.sleep(0.5)
    except Exception as e:
        print(e)

    # link, date, stars, res, team1, team2, p11-p25
    with open('allMatchesInfo.pickle', 'wb') as f:
        pickle.dump(lines, f)


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
        sys.stdout.write("\r{0}".format((f'{i}/200')))
        time.sleep(0.5)

    with open('allMatchLinks.pickle', 'wb') as f:
        pickle.dump(allMatchLinks, f)
    print('done')


def getRang(URL):
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


if __name__ == "__main__":
    # getRang("https://www.hltv.org/team/10672/vertex")
    # getAllMatches("https://www.hltv.org/results?offset=")
    # getPickleData('allMatchLinks.pickle')
    getMatchInfo()
    getPickleData('allMatchesInfo.pickle', True)
