import pandas as pd


HOST = "https://www.hltv.org"
PLAYERS_STAT = "https://www.hltv.org/stats/players/"

MAPS_DICT = ['Cache', 'Season', 'Dust2', 'Mirage', 'Inferno', 'Nuke', 'Train', 'Cobblestone', 'Overpass', 'Tuscan', 'Vertigo', 'Ancient']
HLTV_MAPS_DICT = {'Cache': "de_cache", 'Season': "de_season", 'Dust2': "de_dust2", 'Mirage': "de_mirage",
                  'Inferno': "de_inferno", 'Nuke': "de_nuke", 'Train': "de_train", 'Cobblestone': "de_cobblestone",
                  'Overpass': "de_overpass", 'Tuscan': "de_tuscan", 'Vertigo': "de_vertigo", 'Ancient': "de_ancient"
                  }


completeTable = pd.DataFrame(data=None, index=None,
columns=['stars', 'mapNum',
'rang1', 'winrate1', 'mapWinrate1', 'mapCount1', 'totalRounds1', 'winOpens1', 'loseOpen1',
'rang2', 'winrate2', 'mapWinrate2', 'mapCount2', 'totalRounds2', 'winOpens2', 'loseOpen2',
'rating11', 'kd11', 'dpr11', 'kpr11', 'apr11', 'depr11', 'ratingMap11', 'kdMap11', 'dprMap11', 'kprMap11', 'aprMap11', 'deprMap11',
'rating12', 'kd12', 'dpr12', 'kpr12', 'apr12', 'depr12', 'ratingMap12', 'kdMap12', 'dprMap12', 'kprMap12', 'aprMap12', 'deprMap12',
'rating13', 'kd13', 'dpr13', 'kpr13', 'apr13', 'depr13', 'ratingMap13', 'kdMap13', 'dprMap13', 'kprMap13', 'aprMap13', 'deprMap13',
'rating14', 'kd14', 'dpr14', 'kpr14', 'apr14', 'depr14', 'ratingMap14', 'kdMap14', 'dprMap14', 'kprMap14', 'aprMap14', 'deprMap14',
'rating15', 'kd15', 'dpr15', 'kpr15', 'apr15', 'depr15', 'ratingMap15', 'kdMap15', 'dprMap15', 'kprMap15', 'aprMap15', 'deprMap15',
'rating21', 'kd21', 'dpr21', 'kpr21', 'apr21', 'depr21', 'ratingMap21', 'kdMap21', 'dprMap21', 'kprMap21', 'aprMap21', 'deprMap21',
'rating22', 'kd22', 'dpr22', 'kpr22', 'apr22', 'depr22', 'ratingMap22', 'kdMap22', 'dprMap22', 'kprMap22', 'aprMap22', 'deprMap22',
'rating23', 'kd23', 'dpr23', 'kpr23', 'apr23', 'depr23', 'ratingMap23', 'kdMap23', 'dprMap23', 'kprMap23', 'aprMap23', 'deprMap23',
'rating24', 'kd24', 'dpr24', 'kpr24', 'apr24', 'depr24', 'ratingMap24', 'kdMap24', 'dprMap24', 'kprMap24', 'aprMap24', 'deprMap24',
'rating25', 'kd25', 'dpr25', 'kpr25', 'apr25', 'depr25', 'ratingMap25', 'kdMap25', 'dprMap25', 'kprMap25', 'aprMap25', 'deprMap25',
])
# 135 columns
# 40000 matches * 10 players * 2 type stats(all maps and specific)
# 40000 matches * 2 teams * 2 page of stat(rang and complete stat)
# 960000 total pages

#testTable = pd.DataFrame(data=None, index=None,
columns = ['link', 'date', 'stars',
         'map1', 'score1', 'map2', 'score2', 'map3', 'score3', 'map4', 'score4', 'map5', 'score5',
         'team1', 'team2',
         'p11', 'p12', 'p13', 'p14', 'p15', 'p21', 'p22', 'p23', 'p24', 'p25'
           ]

columnsPlayersStatExcel = ['link', 'date', 'stars', 'map', 'score', 'winner', 'mapNum', 'team1', 'team2',
'nickname11', 'linkAllStat11',  'rating11', 'kd11', 'dpr11', 'kpr11', 'apr11', 'depr11', 'linkMapStat11', 'ratingMap11', 'kdMap11', 'dprMap11', 'kprMap11', 'aprMap11', 'deprMap11',
'nickname12', 'linkAllStat12',  'rating12', 'kd12', 'dpr12', 'kpr12', 'apr12', 'depr12', 'linkMapStat12', 'ratingMap12', 'kdMap12', 'dprMap12', 'kprMap12', 'aprMap12', 'deprMap12',
'nickname13', 'linkAllStat13',  'rating13', 'kd13', 'dpr13', 'kpr13', 'apr13', 'depr13', 'linkMapStat13', 'ratingMap13', 'kdMap13', 'dprMap13', 'kprMap13', 'aprMap13', 'deprMap13',
'nickname14', 'linkAllStat14',  'rating14', 'kd14', 'dpr14', 'kpr14', 'apr14', 'depr14', 'linkMapStat14', 'ratingMap14', 'kdMap14', 'dprMap14', 'kprMap14', 'aprMap14', 'deprMap14',
'nickname15', 'linkAllStat15',  'rating15', 'kd15', 'dpr15', 'kpr15', 'apr15', 'depr15', 'linkMapStat15', 'ratingMap15', 'kdMap15', 'dprMap15', 'kprMap15', 'aprMap15', 'deprMap15',
'nickname21', 'linkAllStat21',  'rating21', 'kd21', 'dpr21', 'kpr21', 'apr21', 'depr21', 'linkMapStat21', 'ratingMap21', 'kdMap21', 'dprMap21', 'kprMap21', 'aprMap21', 'deprMap21',
'nickname22', 'linkAllStat22',  'rating22', 'kd22', 'dpr22', 'kpr22', 'apr22', 'depr22', 'linkMapStat22', 'ratingMap22', 'kdMap22', 'dprMap22', 'kprMap22', 'aprMap22', 'deprMap22',
'nickname23', 'linkAllStat23',  'rating23', 'kd23', 'dpr23', 'kpr23', 'apr23', 'depr23', 'linkMapStat23', 'ratingMap23', 'kdMap23', 'dprMap23', 'kprMap23', 'aprMap23', 'deprMap23',
'nickname24', 'linkAllStat24',  'rating24', 'kd24', 'dpr24', 'kpr24', 'apr24', 'depr24', 'linkMapStat24', 'ratingMap24', 'kdMap24', 'dprMap24', 'kprMap24', 'aprMap24', 'deprMap24',
'nickname25', 'linkAllStat25',  'rating25', 'kd25', 'dpr25', 'kpr25', 'apr25', 'depr25', 'linkMapStat25', 'ratingMap25', 'kdMap25', 'dprMap25', 'kprMap25', 'aprMap25', 'deprMap25',
                           ]
