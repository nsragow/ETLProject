print("start")
import pandas as pd
import sqlite3

def query(c,query):
    c.execute("""SELECT HomeTeam, sum(FTHG) as HomeGoals FROM Matches WHERE Season == 2011 GROUP BY HomeTeam""")
    df = pd.DataFrame(c.fetchall())
    df.columns = [x[0] for x in c.description] #home team goals
    return df
def create_goals(df_home,df_away):
    df_goals = pd.concat([df_home, df_away], sort=False, axis=1)
    df_goals['Total_Goals'] = df_goals.HomeGoals + df_goals.AwayGoals
    df_goals.drop(['HomeTeam', 'HomeGoals', 'AwayGoals'], axis=1, inplace=True)
    df_goals.columns = ['Teams', 'Total_Goals']
    return df_goals
def collect_all_dfs():
    #home team goals
    global df_home
    df_home = query(c,"""SELECT HomeTeam, sum(FTHG) as HomeGoals FROM Matches WHERE Season == 2011 GROUP BY HomeTeam""")
    #away team goals
    global df_away
    df_away = query(c,"""SELECT AwayTeam, sum(FTAG) as AwayGoals FROM Matches WHERE Season == 2011 GROUP BY AwayTeam""")
    #home team wins
    global df_hwins
    df_hwins = query(c,"""SELECT HomeTeam, count(FTR) AS Wins FROM Matches WHERE Season == 2011 and FTR == 'H' GROUP BY HomeTeam """)
    #home team losses
    global df_hlosses
    df_hlosses = query(c,"""SELECT HomeTeam AS Team, count(FTR) As Losses FROM Matches WHERE Season == 2011 and FTR == 'A' GROUP BY HomeTeam""")
    #Away team wins
    global df_awins
    df_awins = query(c,"""SELECT AwayTeam, count(FTR) AS Win FROM Matches WHERE Season == 2011 and FTR == 'A' GROUP BY AwayTeam""")
    #Away team losses
    global df_alosses
    df_alosses = query(c,"""SELECT AwayTeam AS Team, count(FTR) AS AwayLosses FROM Matches WHERE Season == 2011 and FTR == 'H'GROUP BY AwayTeam""")
    #home team losses
    global df_d
    df_d = query(c,"""SELECT count(FTR) As Draw FROM Matches WHERE Season == 2011 and FTR == 'D' GROUP BY HomeTeam""")

conn = sqlite3.connect('database.sqlite')
c = conn.cursor()

collect_all_dfs()


df_goals = create_goals(df_home,df_away)

total_losses = df_alosses.merge(df_hlosses, how='left')

wins = pd.concat([df_hwins, df_awins], axis=1)
wins['Total_Wins'] = wins['Wins'] + wins['Win']
wins.drop(['Wins', 'AwayTeam', 'Win'], axis=1, inplace=True)

losses = pd.concat([df_alosses, df_hlosses],join='inner', axis=1)
total_losses.Losses.fillna(0, inplace=True)
total_losses['Total_Losses'] = total_losses['AwayLosses'] + total_losses['Losses']
total_losses.drop(['AwayLosses', 'Losses'], axis=1, inplace=True)

df_2011 = pd.concat([wins, total_losses, df_goals, ], axis=1)
df_2011.drop(['Team','Teams'], axis=1, inplace=True)

df_2011.columns = ['name', '2011_wins', '2011_losses', '2011_goals']

df_2011['win_rate'] = df_2011['2011_wins']/(df_2011['2011_wins'] + df_2011['2011_losses'] + df_d['Draw'])

df_2011.columns = ['name', '2011_wins', '2011_losses', '2011_goals', 'win_rate']
print(df_2011.head())
print("hi")
