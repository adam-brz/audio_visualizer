import os

import aud
import numpy as np


class AudioData:
    def __init__(self):
        self._audio_path = ""
        self._audio_file_modification_time = None
        self._cached_audio = None
        self._cached_data = None

    def load(self, audio_path):
        modification_time = os.path.getmtime(audio_path)

        if (
            audio_path == self._audio_path
            and self._audio_file_modification_time == modification_time
        ):
            return

        self._audio_file_modification_time = modification_time
        self._audio_path = audio_path
        self._cached_audio = aud.Sound.cache(aud.Sound(self._audio_path))
        self._cached_data = self._cached_audio.data()

        channels = self._cached_audio.specs[1]
        if channels > 1:
            self._cached_data = np.average(self._cached_data, axis=1)

    def data(self):
        return self._cached_data

    def freq(self):
        return self._cached_audio.specs[0]
