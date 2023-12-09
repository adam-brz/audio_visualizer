from .audio_data import AudioData

import numpy as np
from dataclasses import dataclass

@dataclass
class ProcessingSettings:
    step_duration_s: float = 1e-3
    frequency_bands: int = 80
    start_freq: float = 60
    end_freq: float = 18000
    use_log_y: bool = True

class AudioProcessor:
    def _find_nearest_idx(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    def process(self, audio_data: AudioData, settings: ProcessingSettings):
        raw_data = audio_data.data()

        samples_count = int(audio_data.freq() * settings.step_duration_s)
        processing_steps_count = raw_data.size // samples_count

        freq_bands = np.fft.fftfreq(samples_count, d=1.0/audio_data.freq())
        output_amp = np.empty((processing_steps_count, settings.frequency_bands))

        for i in range(processing_steps_count):
            window_data = raw_data[i * samples_count: (i + 1) * samples_count]
            fourier = np.fft.rfft(window_data)

            start_freq_idx = self._find_nearest_idx(freq_bands, settings.start_freq)
            end_freq_idx = self._find_nearest_idx(freq_bands, settings.end_freq)
            amplitude = np.abs(fourier[start_freq_idx:end_freq_idx])

            if amplitude.size <= 0:
                continue

            frequency_band_size = amplitude.size // settings.frequency_bands
            aligned_amp = amplitude[:(len(amplitude) // frequency_band_size) * frequency_band_size]
            avg_amp_bands = np.mean(aligned_amp.reshape(-1, frequency_band_size), axis=1)
            output_amp[i, :] = avg_amp_bands[:settings.frequency_bands]

        if settings.use_log_y:
            output_amp = np.log10(output_amp + 1)

        return output_amp