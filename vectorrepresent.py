# VectorRespresent.py
# File that takes care of converting an audio representation to vector representation

import numpy, scipy, matplotlib.pyplot as plt
import librosa, librosa.display


# x, sr = librosa.load('Data/midi-synth/BohemianRhapsody.wav')
x, sr = librosa.load('Data/audio/BohemianRhapsody.wav')

hop_length = 512


chromagram = librosa.feature.chroma_cqt(x, sr=sr, hop_length=hop_length)

print(chromagram)

plt.figure(figsize=(15, 5))
librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', hop_length=hop_length, cmap='coolwarm')
plt.show()
