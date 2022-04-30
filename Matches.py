import json
import pickle
import time

import os
import sys

from collections import OrderedDict

import requests
from bs4 import BeautifulSoup

import PickleFiles
import Players
import constants


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
            allMatchLinks.append([f"{constants.HOST}{link}", len(stars)])  # add this info to list

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
    allMatchLinks = PickleFiles.getPickleData('allMatchLinks.pickle')
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
            team1 = constants.HOST + soup.find('div', {"class": "team1-gradient"}).find('a').get('href')
            team2 = constants.HOST + soup.find('div', {"class": "team2-gradient"}).find('a').get('href')
            date = soup.find('div', {"class": "date"}).get('data-unix')

            # try, cause some matches are didn't play (ex map: Default, score 1-0)
            try:
                # find all players
                players = soup.find('div', {'class': 'lineups'}).find_all('td', {"class": 'player'})
                for j in range(len(players)):
                    players[j] = constants.HOST + str(players[j].find('a').get('href'))
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
                PickleFiles.addToFile(os.path.join('Logs', f'{i}.html', soup.prettify()), 'w')  # save page
        finally:
            i += 1
        if (i + 1) % 100 == 0:
            # link, date, stars, res, team1, team2, p11-p25
            with open(os.path.join('MatchData', f'allMatchesInfo-{i + 1}.pickle'), 'wb') as f:
                pickle.dump(lines, f)
            lines = []


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
