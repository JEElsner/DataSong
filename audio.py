from pyo import *
import time
import numpy as np


class AudioManager:
    def __init__(self):
        self.server = Server(winhost='mme')
        self.server.boot().start()

        self.tone = Sine(0, 0, 0.1)
        self.tone.out()

    def setFreq(self, freq):
        self.tone.setFreq(float(freq))

    def stop(self):
        self.server.stop()

    def __del__(self):
        self.stop()


def play_freqs(freqs, bpm):
    freqs = freqs.astype(float)
    sec_per_beat = 60 / bpm

    s = Server(winhost='mme')
    s.boot()
    s.start()

    a = Sine(float(freqs[0]), 0, 0.1)
    a.out()

    for f in freqs:
        a.setFreq(float(f))
        # We really don't have to be precise about how long we're sleeping right now
        time.sleep(sec_per_beat)

    s.stop()
