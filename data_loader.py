import converter
import audio

import csv
from typing import List

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import tkinter

file_path = 'SP500.csv'
x_axis_column_name = 'DATE'
data_column_name = 'SP500'

data_slice = slice(-30, None, 1)
num_of_labels = 20

song_duration = 2  # two minutes


def transpose_data(csv_dict):
    out = {}

    for row in csv_dict:
        for key in row.keys():
            if key not in out.keys():
                out.update({key: []})

            out[key].append(row[key])

    return out


def to_func(dict_data):
    '''
    Relates an input dataset to 
    '''

    key_list = list(dict_data.keys())
    input_key = key_list[0]

    out = {}

    for key in key_list[1:]:
        out.update({key: {}})

        for x, y in zip(dict_data[input_key], dict_data[key]):
            out[key].update({x: y})

    return out


def apply_slice_to_all(datasets, s: slice):
    for k, v in datasets.items():
        datasets[k] = v[s]

    return datasets


def convert_to_float(data):
    last = 0

    def try_parse_float(x):
        global last

        try:
            last = float(x)
            return last
        except ValueError:
            return last

    return (try_parse_float(x) for x in data)


def play_with_graph(datasets):
    relationship = to_func(datasets)

    fig, ax = plt.subplots()
    line, = plt.plot([], [])

    yrs_per_x_interval = int(len(datasets[x_axis_column_name]) / num_of_labels)
    plt.xticks(range(0, len(
        datasets[x_axis_column_name]), yrs_per_x_interval), datasets[x_axis_column_name][::yrs_per_x_interval], rotation=45)

    plt.subplots_adjust(bottom=0.2)

    xdata: List[str] = []
    ydata: List[float] = []

    ax.set_xlim(0, len(datasets[x_axis_column_name]))
    ax.set_ylim(min(datasets[data_column_name]) * 0.9,
                max(datasets[data_column_name]) * 1.1)

    plt.ion()
    plt.show()
    audio_manager = audio.AudioManager()

    def win_close(evt):
        audio_manager.stop()
        exit()
    fig.canvas.mpl_connect('close_event', win_close)

    for date in datasets[x_axis_column_name]:
        xdata.append(date)
        ydata.append(relationship[x_axis_column_name][date])
        audio_manager.setFreq(relationship['FREQUENCY'][date])
        line.set_data(range(0, len(ydata)), ydata)

        try:
            plt.pause(note_length)
        except tkinter.TclError:
            break

    audio_manager.stop()

    input("Press ENTER to continue...")


with open(file_path, mode='r') as csv_file:
    csv_dict = csv.DictReader(csv_file)

    datasets = transpose_data(csv_dict)
    datasets[data_column_name] = list(
        convert_to_float(datasets[data_column_name]))
    datasets = apply_slice_to_all(datasets, data_slice)

    data_arr = np.array(datasets[data_column_name])

    notes = converter.to_notes(data_arr)
    datasets.update({'NOTE': list(notes)})

    freqs = converter.frequency(notes)
    datasets.update({'FREQUENCY': list(freqs)})

    bpm = len(data_arr) / song_duration
    if bpm < 120:
        bpm = 120
    note_length = 60 / bpm

    print('{0} notes\n{1} minutes\n{2} bpm\n'.format(
        len(notes), song_duration, bpm))

    play_with_graph(datasets)
