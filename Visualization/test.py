import pandas as pd
from visualization import append_visualizations

rows = []
for x in range(100):
    rows.append(["team_name",10,5])
df = pd.DataFrame(data=rows,columns=["name","2011_wins","2011_losses"])

append_visualizations(df)

print(df.head())
