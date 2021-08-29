from typing import Tuple
from typing import Optional
import time
import pyaudio
import threading
import numpy as np
import tkinter as tk

from chinese_shadowing.plot import plot_amplitude
from chinese_shadowing.utilities import get_time


CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
TIMEOUT = 10
PLOT = False


class RecordAudioThread(threading.Thread):
    """Thread that record raw audio in numpy array form"""
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
        print(f'{get_time()} Start recording')  # todo need to put it outside + indicator
        frames = []
        start_time = time.time()
        current_time = time.time()

        while ((current_time - start_time) < TIMEOUT and not self._stop_event.isSet()) or not frames:
            data = self.stream.read(CHUNK)
            frames.append(np.frombuffer(data, dtype=np.int16))
            current_time = time.time()

        self._recording = np.hstack(frames)
        self.stream.close()
        self.p.terminate()
        print(f'{get_time()} Stop recording')  # todo need to put it outside

    def join(
            self,
            timeout: Optional[int] = None
    ) -> Tuple[np.array, int, int]:
        """set stop event and join within a given time period"""
        self._stop_event.set()
        super().join(timeout)
        return self._recording, RATE, CHANNELS


class Recorder:
    """Class that made the creation of recording threads easy for tkinter"""
    def __init__(self):
        self.thread = None
        self.result = None
        self._key_pressed = False

    def start(self, event : Optional[tk.Event] = None):
        if not self._key_pressed:
            self.thread = RecordAudioThread()
            self.thread.start()
        self._key_pressed = True

    def stop(self, event : Optional[tk.Event] = None):
        if self._key_pressed:
            self.result = self.thread.join()
            if PLOT and self.result[0] is not None:
                plot_amplitude(self.result[0], rate=RATE * 2, title='test recording')
        self._key_pressed = False


if __name__ == '__main__':
    master = tk.Tk()
    recorder = Recorder()
    master.bind("<KeyPress-k>", recorder.start)
    master.bind("<KeyRelease-k>", recorder.stop)
    master.mainloop()
