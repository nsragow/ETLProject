import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
#name  2011_wins  2011_losses






def save_win_loss(wins,losses):
    '''
    Takes a win count and loss count and converts them into a Seaborn
    barplot

    Params:
        wins:
            Integer count of wins
        losses:
            Integer count of losses
    Return:
        BytesIO containing the byte representation of the
        png file of the Seaborn barplot
    '''
    sns.barplot(["wins","losses"],[wins,losses])
    ioO = io.BytesIO()
    plt.savefig(ioO, bbox_inches='tight')
    return ioO
def append_visualizations(df):
    '''
    Takes a pandas dataframe and adds a column containing a png representation
    of the win/loss counts (in binary).

    Params:
        df:
            Pandas dataframe containing integer columns '2011_wins' and '2011_losses'
    '''
    df["visualization_png_binary"] = df.apply(row_to_visualization,axis=1)
def row_to_visualization(row):
    '''
    Takes a formatted Pandas row and returs the png.
    see append_visualizations

    Params:
        row:
            the Pandas row
    '''
    data = save_win_loss(row["2011_wins"],row["2011_losses"])
    data.seek(0)
    byte = None
    byte_string = b""
    while byte != b"":
        byte = data.read(1)
        byte_string += byte
    data.close()
    return byte_string
