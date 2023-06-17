import matplotlib.pyplot as plt  
import pandas as pd
import numpy as np
import sys

LEN_OF_SIGAL_TO_DISPLAY = 7000

def main(csv_path):
    dataframe = pd.read_csv(csv_path, sep=';')
    len_of_signal = len(dataframe)
    len_of_signal_to_display = len_of_signal if len_of_signal < LEN_OF_SIGAL_TO_DISPLAY else LEN_OF_SIGAL_TO_DISPLAY
    starts_of_rep_positions = [pos for pos in np.where(dataframe.FLAG==1)[0] if pos < len_of_signal_to_display]
    columns = ["PITCH", "ROLL", "YAW"]
    fig, ax = plt.subplots(figsize=(12, 6))
    for col in columns:
        ax.plot(range(len_of_signal_to_display), dataframe[col][0:len_of_signal_to_display], label=col)
    for pos in starts_of_rep_positions:
        ax.axvline(pos, color="red")
    ax.set_xlabel("Time", fontsize=15)
    ax.set_ylabel("Value", fontsize=15)
    ax.set_title('Result', fontweight='bold', fontsize=15)
    ax.legend(prop={'size':13}, loc='lower right')
    fig, axs = plt.subplots(len(columns), 1, figsize=(12, 6*len(columns)), sharex=True)
    for i, col in enumerate(columns):
        axs[i].plot(range(len_of_signal_to_display), dataframe[col][0:len_of_signal_to_display])
        axs[i].set_ylabel(col, fontsize=15)
        for pos in starts_of_rep_positions:
            axs[i].axvline(pos, color="red")
    axs[-1].set_xlabel("Time", fontsize=15)
    fig.suptitle('Result', fontweight='bold', fontsize=15)
    plt.show()

if __name__ == "__main__":
    csv_path = sys.argv[1]
    main(csv_path)
