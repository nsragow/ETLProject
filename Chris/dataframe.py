import pandas as pd
import numpy as np
import sqlite3
import requests as r
import json


import sys
sys.path.append('./DarkSkyAPI')


from dailyconditions import TimeMachine

def data(database):
    '''
    Params:
        database:
            String path to sqlite file
    '''
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("""SELECT * FROM Matches WHERE Season == 2011 and Div == 'D1' ORDER BY Date """)
    df = pd.DataFrame(c.fetchall())
    df.columns = [x[0] for x in c.description]
    return df #returns dataframe with all Division 1 teams from the 2011 season

def dates_to_integers(dataframe):
    dates = []
    for i in range(len(dataframe.Date)):
        dates.append(dataframe.Date[i].split('-')) #split the year, month, day apart
    Dates = []
    for i in range(len(dates)):
        Dates.append(list(map(int, dates[i]))) #change the dates to integers


def rain_days(dark_sky_api_key): #returns either 'rain' or 'none' for each date
    rainy_days = []
    tm = TimeMachine(dark_sky_api_key)
    for row in Dates:
        response = tm.time_to_label_with_json(row[0],row[1],row[2])
        print(response[0]) #precipitation label
        rainy_days.append(response[0])



def rainy_day_wins(dataframe):
    germany_df = dataframe
    germany_df['rainy_days'] = rainy_days #adds the rainy_days list created in the previous function to the new data frame
    germany_df['rainy_wins'] = rainy_wins
    team_names = set(germany_df.HomeTeam)
    rainy_wins = np.zeros(306,dtype=int)
#fills the rainy_wins column with the team that won if the corresponding rain_days column has a value of 'rain' otherwise none
    for i in range(len(germany_df)):
        if germany_df['FTR'][i] == 'H' and germany_df['rainy_days'][i] == 'rain':
            germany_df['rainy_wins'][i] = germany_df.HomeTeam[i]
        if germany_df['FTR'][i] == 'A' and germany_df['rainy_days'][i] == 'rain':
            germany_df['rainy_wins'][i] = germany_df.AwayTeam[i]
        else:
            germany_df['rainy_wins'][i] = None

    germany_dict_list = []
#for loop returns a list of dictionaries with the keys: 'name', '2011_wins', '2011_losses', '2011_goals', 'win_rate_on_rainy_days'
    for team in team_names:
        team_dict = {}
        team_dict['name'] = team
        home_wins = sum(germany_df[germany_df.HomeTeam == team]['FTR'] == 'H')
        away_wins = sum(germany_df[germany_df.AwayTeam == team]['FTR'] == 'A')
        home_losses =  sum(germany_df[germany_df.HomeTeam == team]['FTR'] == 'A')
        away_losses =  sum(germany_df[germany_df.AwayTeam == team]['FTR'] == 'H')
        home_goals = sum(germany_df[germany_df.HomeTeam == team]['FTHG'])
        away_goals = sum(germany_df[germany_df.AwayTeam == team]['FTAG'])
        team_dict['2011_wins'] = home_wins + away_wins
        team_dict['2011_losses'] = away_losses + home_losses
        team_dict['2011_goals'] = home_goals + away_goals
        team_dict['win_rate_on_rainy_days'] = sum(germany_df['rainy_wins'] == team)/34
        germany_dict_list.append(team_dict)

        final_df = pd.DataFrame(germany_dict_list) #change the list of dictionaries to dataframe
        return final_df
