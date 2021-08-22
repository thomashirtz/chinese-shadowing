import time
import pyaudio
import numpy as np
import tkinter as tk
from chinese_shadowing.plot import plot_amplitude
import threading

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
TIMEOUT = 10
PLOT = True


class RecordAudioThread(threading.Thread):
    # https://stackoverflow.com/questions/18018033/how-to-stop-a-looping-thread-in-python
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.p = pyaudio.PyAudio()
        self._recording = None
        self.stream = self.p.open(
            format=FORMAT,
            channels=2,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK,
        )

    def run(self):
        print('start recording')
        frames = []
        start_time = time.time()
        current_time = time.time()

        while (current_time - start_time) < TIMEOUT and not self._stop_event.isSet():
            data = self.stream.read(CHUNK)
            frames.append(np.frombuffer(data, dtype=np.int16))
            current_time = time.time()
        self._recording = np.hstack(frames)
        self.stream.close()
        self.p.terminate()

    def join(self, timeout=None):
        """set stop event and join within a given time period"""
        self._stop_event.set()
        super().join(timeout)
        return self._recording, RATE, CHANNELS


class Recorder:
    def __init__(self):
        self._key_pressed = False
        self.thread = None
        self.result = None

    def start(self, event):
        if not self._key_pressed:
            self.thread = RecordAudioThread()
            self.thread.start()
        self._key_pressed = True

    def stop(self, event):
        if self._key_pressed:
            self.result = self.thread.join()
            if PLOT:
                plot_amplitude(self.result[0], rate=RATE * 2, title='test recording')
        self._key_pressed = False


if __name__ == '__main__':
    master = tk.Tk()
    listener = Recorder()
    master.bind("<KeyPress-k>", listener.start)
    master.bind("<KeyRelease-k>", listener.stop)
    master.mainloop()
