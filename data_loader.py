import converter
import audio

from typing import List

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import tkinter

# === Configuration === #

file_path = 'SP500.csv'  # Path to data

# name of the column in the specified file containing the data
data_col = 'SP500'

data_slice = slice(None, None, 1)
num_of_labels = 20

song_duration = .5  # in minutes


def visualize(dataset, note_length):
    '''
    Creates an animated plot of the data while the generated notes play

    Arguments:

        dataset     Pandas dataframe containing the data and frequencies. The
            data should be in the column specified by data_col, and the
            frequencies should be in the column 'FREQUENCIES'

        note_length How long in seconds to play each note
    '''

    # Matplotlib initialization
    fig, ax = plt.subplots()
    line, = plt.plot([], [])

    # yrs_per_x_interval = int(len(dataset) / num_of_labels)
    # plt.xticks(range(0, len(dataset), yrs_per_x_interval),
    #            dataset.iloc[::yrs_per_x_interval], rotation=45)

    # Configure plot to get the spacing right for dates
    plt.subplots_adjust(bottom=0.2)

    # Set up variables to manage animation
    xdata: List[str] = []
    ydata: List[float] = []

    # Set bounds of th graph
    ax.set_xlim(0, len(dataset))
    ax.set_ylim(min(dataset[data_col]) * 0.8,
                max(dataset[data_col]) * 1.1)

    # Begin animation
    plt.ion()
    plt.show()
    audio_manager = audio.AudioManager()

    # Create callback to manage exit commands
    def win_close(evt):
        audio_manager.stop()
        exit()
    fig.canvas.mpl_connect('close_event', win_close)

    # Loop through the animation
    for date in dataset.index:
        # Update the graph data
        xdata.append(date)
        ydata.append(dataset.loc[date, data_col])

        # Update the output sound
        audio_manager.setFreq(dataset.loc[date, 'FREQUENCY'])

        # Update the graph
        line.set_data(range(0, len(ydata)), ydata)

        # Play the note for its intended time
        try:
            plt.pause(note_length)  # Hmmm, this accesses a global variable...
        except tkinter.TclError:
            break

    # Stop playing audio out
    audio_manager.stop()

    # Keep the graph window open until it is closed
    input("Press ENTER to continue...")


if __name__ == '__main__':
    # Read input data
    dataset = pd.read_csv(file_path,
                          index_col=0,
                          parse_dates=True,
                          dtype={data_col: np.float64},
                          na_values='.')

    # Ignore NaN values
    dataset.dropna(subset=[data_col], inplace=True)

    # Slice data to only take the range we want
    dataset = dataset.iloc[data_slice]

    # Process data into numerical notes and frequencies
    dataset['NOTE'] = converter.to_notes(dataset[data_col])
    dataset['FREQUENCY'] = converter.frequency(dataset['NOTE'])

    # Output the processed data into a CSV
    dataset.to_csv('parsed_dataset.csv')

    # Play the song
    bpm = len(dataset) / song_duration
    if bpm < 120:
        bpm = 120
    note_length = 60 / bpm

    print('{0} notes\n{1} minutes\n{2} bpm\n'.format(
        len(dataset), song_duration, bpm))

    visualize(dataset, note_length)
