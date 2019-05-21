import pandas as pd




def get_without_viz():
    rows = []
    for x in range(50):
        row = []
        for y in range(5):
            row.append(10)
        rows.append(row)
    columns = ["name","2011_wins","2011_losses","win_rate_on_rainy_days","2011_goals"]

    df = pd.DataFrame(data=rows,columns=columns)
    return df
