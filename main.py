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

import PickleFiles
import Players
import Matches
import constants


def test():
    data = PickleFiles.getPickleData("tempData.pkl")
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
    Players.getPlayersStat()
    #Players.converToExcel()
    # test()
    # getPickleData(os.path.join('MatchData',f'allMatchesInfo-10.pickle'), True)
