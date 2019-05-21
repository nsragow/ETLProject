import pandas as pd
import sqlite3

conn = sqlite3.connect('database.sqlite')
c = conn.cursor()



c.execute("""SELECT HomeTeam, sum(FTHG) as HomeGoals FROM Matches WHERE Season == 2011 GROUP BY HomeTeam""")
df_home = pd.DataFrame(c.fetchall())
df_home.columns = [x[0] for x in c.description] #home team goals

c.execute("""SELECT AwayTeam, sum(FTAG) as AwayGoals FROM Matches WHERE Season == 2011 GROUP BY AwayTeam""")
df_away = pd.DataFrame(c.fetchall())
df_away.columns = [x[0] for x in c.description] #away team goals
df_goals = pd.concat([df_home, df_away], sort=False, axis=1)
df_goals['Total_Goals'] = df_goals.HomeGoals + df_goals.AwayGoals
df_goals.drop(['HomeTeam', 'HomeGoals', 'AwayGoals'], axis=1, inplace=True)
df_goals.columns = ['Teams', 'Total_Goals']

c.execute("""SELECT HomeTeam, count(FTR) AS Wins FROM Matches WHERE Season == 2011 and FTR == 'H' GROUP BY HomeTeam """)
df_hwins = pd.DataFrame(c.fetchall())
df_hwins.columns = [x[0] for x in c.description]  #home team wins

c.execute("""SELECT HomeTeam AS Team, count(FTR) As Losses FROM Matches WHERE Season == 2011 and FTR == 'A' GROUP BY HomeTeam""")
df_hlosses = pd.DataFrame(c.fetchall())
df_hlosses.columns = [x[0] for x in c.description]  #home team losses


c.execute("""SELECT AwayTeam, count(FTR) AS Win FROM Matches WHERE Season == 2011 and FTR == 'A' GROUP BY AwayTeam""")
df_awins = pd.DataFrame(c.fetchall())
df_awins.columns = [x[0] for x in c.description]  #Away team wins

c.execute("""SELECT AwayTeam AS Team, count(FTR) AS AwayLosses FROM Matches WHERE Season == 2011 and FTR == 'H'GROUP BY AwayTeam""")
df_alosses = pd.DataFrame(c.fetchall())
df_alosses.columns = [x[0] for x in c.description] #Away team losses

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
c.execute("""SELECT count(FTR) As Draw FROM Matches WHERE Season == 2011 and FTR == 'D' GROUP BY HomeTeam""")
df_d = pd.DataFrame(c.fetchall())
df_d.columns = [x[0] for x in c.description]  #home team losses

df_2011['win_rate'] = df_2011['2011_wins']/(df_2011['2011_wins'] + df_2011['2011_losses'] + df_d['Draw'])


df_2011.columns = ['name', '2011_wins', '2011_losses', '2011_goals', 'win_rate']
