import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
#name  2011_wins  2011_losses






def save_win_loss(wins,losses):
    sns.barplot(["wins","losses"],[wins,losses])
    ioO = io.BytesIO()
    plt.savefig(ioO, bbox_inches='tight')
    return ioO
def append_visualizations(df):
    df["visualization_png_binary"] = df.apply(row_to_visualization,axis=1)
def row_to_visualization(row):

    data = save_win_loss(row["2011_wins"],row["2011_losses"])
    data.seek(0)
    byte = None
    byte_string = b""
    while byte != b"":
        byte = data.read(1)
        byte_string += byte
    data.close()
    return byte_string
