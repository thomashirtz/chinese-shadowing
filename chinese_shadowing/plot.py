import numpy as np
from typing import Optional
import matplotlib.pyplot as plt


def plot_amplitude(audio, rate, title: Optional = None):
    time = np.arange(len(audio)) / rate
    plt.plot(time, audio)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    if title:
        plt.title(label=title)
    plt.show()
