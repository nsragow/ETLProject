import pandas as pd
import numpy as np
import sqlite3
import requests as r
import json

 def data(database):
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

class TimeMachine():
    '''
    Used to get historical data from Dark Sky API.
    Specifically draws out the precipitation type per day.
    Usage:
        tm = TimeMachine(dark_sky_api_key)
        response = tm.time_to_label_with_json(some_year,some_month,some_day)
        #precipitation label#
        print(response[0])
        #full JSON#
        print(response[1])
    '''
    lat = 52.520008
    lon = 13.404954
    def __init__(self, api_key):
        self.api_key = api_key

    def time_to_label_with_json(self,year,month,day):
        day = "{:0>2d}".format(day)
        month = "{:0>2d}".format(month)
        year = "{}".format(year)

        time = f"{year}-{month}-{day}T13:00:00"

        https = f"https://api.darksky.net/forecast/{self.api_key}/{self.lat},{self.lon},{time}?exclude=minutely,hourly,flags,currently"

        response = r.get(https)

        response_json = response.json()

        label = None
        err_msg = None
        if "daily" in  response_json.keys():
            #good
            daily = response_json["daily"]
            if "data" in daily:
                data = daily["data"]
                if len(data) > 0:
                    target_data = data[0]
                    if "precipType" in target_data:
                        label = target_data["precipType"]
                    else:
                        label = "none"
                else:
                    err_msg = "ERR: data array was empty"
            else:
                err_msg = "ERR: data not in daily"
        else:
            err_msg = "ERR: 'daily' not in response"

        if err_msg is not None:
            return err_msg
        return (label,response_json)

def rain_days(dark_sky_api_key): #returns either 'rain' or 'none' for each date
    rainy_days = []
    tm = TimeMachine(dark_sky_api_key)
    for row in Dates:
        response = tm.time_to_label_with_json(row[0],row[1],row[2])
        print(response[0]) #precipitation label
        rainy_days.append(response[0])

germany_df = df

def rainy_day_wins(dataframe):
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
