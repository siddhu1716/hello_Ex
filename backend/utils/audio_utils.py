import wave
import struct
import math
from typing import Optional


def generate_dummy_wav(text: str, out_path: str, duration_sec: float = 1.0, freq: float = 440.0, sample_rate: int = 16000) -> None:
    """
    Generate a short sine-tone WAV so we have an audio artifact for the pipeline.
    """
    n_samples = int(duration_sec * sample_rate)
    amplitude = 16000  # 16-bit

    with wave.open(out_path, 'w') as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)

        for i in range(n_samples):
            t = i / sample_rate
            value = int(amplitude * math.sin(2 * math.pi * freq * t))
            wf.writeframes(struct.pack('<h', value))
