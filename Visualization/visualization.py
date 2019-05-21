import matplotlib.pyplot as plt
import seaborn as sns
import os
#name  2011_wins  2011_losses


filename = "file_temp_png_1010101010101010101010101.png"



def save_win_loss(wins,losses,filename):
    sns.barplot(["wins","losses"],[wins,losses])
    plt.savefig(filename, bbox_inches='tight')
def append_visualizations(df):
    global filename
    df["visualization_png_binary"] = df.apply(row_to_visualization,axis=1)
    os.remove(filename)
def row_to_visualization(row):
    global filename
    save_win_loss(row["2011_wins"],row["2011_losses"],filename)
    file = open(filename,"rb")
    byte = None
    byte_string = b""
    while byte != b"":
        byte = file.read(1)
        byte_string += byte
    file.close()
    return byte_string
