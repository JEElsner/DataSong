from pyo import Server, Sine
import time


class AudioManager:
    '''
    AudioManager class to abstract away interaction with the Python audio
    library pyo
    '''

    def __init__(self):
        '''
        Start the audio server and a silent tone
        '''
        self.server = Server(winhost='mme')
        self.server.boot().start()

        # Silent tone with no amplitude, phase shift, and really quiet (0.1)
        self.tone = Sine(0, 0, 0.1)
        self.tone.out()

    def setFreq(self, freq):
        '''
        Change the frequency of the tone
        '''
        self.tone.setFreq(float(freq))

    def stop(self):
        '''
        Stop the audio server
        '''
        self.server.stop()

    def __del__(self):
        # Code to make sure the server stops automatically when we stop using
        # the audio manager class
        self.stop()


def play_freqs(freqs, bpm):
    '''
    Method that just plays the iterator of frequencies provided at the
    specified beats per minute.
    '''
    freqs = freqs.astype(float)
    sec_per_beat = 60 / bpm

    s = Server(winhost='mme')
    s.boot()
    s.start()

    a = Sine(float(freqs[0]), 0, 0.1)
    a.out()

    for f in freqs:
        a.setFreq(float(f))
        # We really don't have to be precise about how long we're sleeping
        # right now
        time.sleep(sec_per_beat)

    s.stop()
