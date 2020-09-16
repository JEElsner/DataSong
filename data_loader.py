import converter
import audio

import csv
from typing import List

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import tkinter

file_path = 'SP500.csv'
x_axis_column_name = 'DATE'
data_column_name = 'SP500'

data_slice = slice(None, None, 1)
num_of_labels = 20

song_duration = .5  # in minutes


def visualize(dataset):

    fig, ax = plt.subplots()
    line, = plt.plot([], [])

    # yrs_per_x_interval = int(len(dataset) / num_of_labels)
    # plt.xticks(range(0, len(dataset), yrs_per_x_interval),
    #            dataset.iloc[::yrs_per_x_interval], rotation=45)

    plt.subplots_adjust(bottom=0.2)

    xdata: List[str] = []
    ydata: List[float] = []

    ax.set_xlim(0, len(dataset))
    ax.set_ylim(min(dataset[data_column_name]) * 0.9,
                max(dataset[data_column_name]) * 1.1)

    plt.ion()
    plt.show()
    audio_manager = audio.AudioManager()

    def win_close(evt):
        audio_manager.stop()
        exit()
    fig.canvas.mpl_connect('close_event', win_close)

    for date in dataset.index:
        xdata.append(date)
        ydata.append(dataset.loc[date, data_column_name])
        audio_manager.setFreq(dataset.loc[date, 'FREQUENCY'])
        line.set_data(range(0, len(ydata)), ydata)

        try:
            plt.pause(note_length)  # Hmmm, this accesses a global variable...
        except tkinter.TclError:
            break

    audio_manager.stop()

    input("Press ENTER to continue...")


if __name__ == '__main__':
    dataset = pd.read_csv('SP500.csv', index_col=0,
                          parse_dates=True, dtype={'SP500': np.float64}, na_values='.')

    dataset.dropna(subset=['SP500'], inplace=True)

    # Slice data to only take the range we want
    dataset = dataset.iloc[data_slice]

    dataset['NOTE'] = converter.to_notes(dataset['SP500'])
    dataset['FREQUENCY'] = converter.frequency(dataset['NOTE'])

    dataset.to_csv('parsed_dataset.csv')

    bpm = len(dataset) / song_duration
    if bpm < 120:
        bpm = 120
    note_length = 60 / bpm

    print('{0} notes\n{1} minutes\n{2} bpm\n'.format(
        len(dataset), song_duration, bpm))

    visualize(dataset)
