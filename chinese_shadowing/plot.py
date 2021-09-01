import numpy as np
from typing import Optional
import matplotlib.pyplot as plt


def plot_amplitude(
        audio: np.array,
        rate: int,
        title: Optional[str] = None
) -> None:
    time = np.arange(len(audio)) / rate
    plt.plot(time, audio)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title(label=title)
    plt.show()
