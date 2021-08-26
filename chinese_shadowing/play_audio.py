from typing import Union
from pathlib import Path

import threading
import numpy as np

from pydub import effects
from pydub import AudioSegment
from pydub.playback import play


def play_audio(
        raw_audio: np.array,
        frame_rate: int,
        channels: int,
        normalize: bool = True
):
    """Play audio that is in numpy array form"""
    audio = AudioSegment(
        raw_audio.tobytes(),
        frame_rate=frame_rate,
        sample_width=raw_audio.dtype.itemsize,
        channels=channels
    )
    if normalize:
        normalized_audio = effects.normalize(audio)
        play(normalized_audio)
    else:
        play(audio)


def get_mp3_audio(file_path: Union[Path, str]):
    """MP3 to numpy array"""
    audio_segment = AudioSegment.from_mp3(file_path)
    raw_audio = np.array(audio_segment.get_array_of_samples())
    raw_audio = raw_audio.reshape((-1, audio_segment.channels))
    return raw_audio, audio_segment.frame_rate, audio_segment.channels


def play_mp3_file(file_path: Union[Path, str]):
    """Play MP3 file"""
    audio, frame_rate, channels = get_mp3_audio(file_path)
    play_audio(audio, frame_rate, channels)


class PlayAudioThread(threading.Thread):
    """Thread that plays raw audio that is in numpy array form"""
    # https://stackoverflow.com/questions/18018033/how-to-stop-a-looping-thread-in-python
    def __init__(self, audio: np.array, frame_rate: int, channels: int):
        threading.Thread.__init__(self)
        self.audio = audio
        self.frame_rate = frame_rate
        self.channels = channels

    def run(self):
        play_audio(self.audio, self.frame_rate, self.channels)

    def join(self, timeout=None):
        """set stop event and join within a given time period"""
        super().join(timeout)
