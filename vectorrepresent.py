# VectorRespresent.py
# File that takes care of converting an audio representation to vector representation

import numpy, scipy, matplotlib.pyplot as plt
import librosa, librosa.display


x, sr = librosa.load('Data/audio/simple_piano.wav')


fmin = librosa.midi_to_hz(36)
hop_length = 512


chromagram = librosa.feature.chroma_cqt(x, sr=sr, hop_length=hop_length)
plt.figure(figsize=(15, 5))
librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', hop_length=hop_length, cmap='coolwarm')