#   Main.py
#
#   File that runs the main pipeline
#
#   Author: David van Erkelens <me@davidvanerkelens.nl, david.vanerkelens@student.uva.nl>

# System includes
import os                               # required for looping over directories
import sys                              # required for redirecting stdout
import pickle                           # required for persistent storage of variables

# Midi-related includes
from midi2audio import FluidSynth       # required for synthesyzting midi's

# Vector-related includes
import librosa, librosa.display         # required for generating chroma vectors
import numpy as np                      # required for vector operations

# Model-related includes
from hmmlearn import hmm                # required to create and test HMMs
from sklearn.externals import joblib    # required to store models

# Visualize-related includes
import matplotlib.pyplot as plt         # required for plots

# Other includes
import operator                         # required for sorting dictionary



hop_length = 2048


def synthMidiFiles():
    print("Checking if all MIDI files are synthesized...")

    path = 'storage/midifiles'
    fs = FluidSynth()
    original = sys.stdout

    for file in os.listdir(path):
        if not os.path.isfile(path + '/' + file):
            continue

        name, ext = file.rsplit('.', 1)

        if ext == 'mid':

            if not os.path.exists('storage/midisynth/' + name + '.wav'):

                print(name + " must still be synthesized")

                sys.stdout = open('storage/synthlog/' + name + '.log', 'w')

                fs.midi_to_audio(path + '/' + file, 'storage/midisynth/' + name + '.wav')

                sys.stdout = original

                print(name + ".wav is created.")

def createMidiChromas():
    print("Checking if all MIDI files have Chroma vectors generated...")

    path = 'storage/midisynth'

    for file in os.listdir(path):
        if not os.path.isfile(path + '/' + file):
            continue

        name, ext = file.rsplit('.', 1)

        if ext == 'wav':
            if not os.path.exists('storage/midichroma/' + name + '.vector'):
                print(name + " must still be converted to chroma vector")

                x, sr = librosa.load('storage/midisynth/' + name + '.wav')

                chromagram = librosa.feature.chroma_cqt(x, sr=sr, hop_length=hop_length)
                pickle.dump(chromagram, open('storage/midichroma/' + name + '.vector', 'wb'))

                print(name + ".vector is created.")

def createAudioChromas():
    print("Checking if all audio files have Chroma vectors generated...")

    path = 'storage/audiofiles'

    for file in os.listdir(path):
        if not os.path.isfile(path + '/' + file):
            continue

        name, ext = file.rsplit('.', 1)

        if ext == 'wav' or ext == 'mp3':
            if not os.path.exists('storage/audiochroma/' + name + '.vector'):
                print(name + " must still be converted to chroma vector")

                x, sr = librosa.load('storage/audiofiles/' + file)


                chromagram = librosa.feature.chroma_cqt(x, sr=sr, hop_length=hop_length)
                pickle.dump(chromagram, open('storage/audiochroma/' + name + '.vector', 'wb'))

                print(name + ".vector is created.")

def visualizeChromaVectors():
    print('Visualizing MIDI-based Chroma vectors')
    for file in os.listdir('storage/midichroma'):

        name, _ = file.rsplit('.', 1)

        plt.figure(figsize=(15, 5))
        librosa.display.specshow(pickle.load(open('storage/midichroma/' + file, 'rb')), x_axis='time', y_axis='chroma', hop_length=hop_length, cmap='coolwarm')
        plt.savefig('storage/midichroma-visual/' + name + '.png')

    print('Visualizing audio-based Chroma vectors')
    for file in os.listdir('storage/audiochroma'):

        name, _ = file.rsplit('.', 1)

        plt.figure(figsize=(15, 5))
        librosa.display.specshow(pickle.load(open('storage/audiochroma/' + file, 'rb')), x_axis='time', y_axis='chroma', hop_length=hop_length, cmap='coolwarm')
        plt.savefig('storage/audiochroma-visual/' + name + '.png')


def createModels():
    print("Checking if all audio files have Hidden Markov Models generated...")

    path = 'storage/audiochroma'

    for file in os.listdir(path):
        if not os.path.isfile(path + '/' + file):
            continue

        name, ext = file.rsplit('.', 1)

        if ext == 'vector':
            if not os.path.exists('storage/models/' + name + '.model'):
                print(name + " has no associated model yet")

                model = hmm .GaussianHMM(n_components=5, covariance_type="full", n_iter=500, algorithm="map",transmat_prior=1.1)
                data = np.array(pickle.load(open('storage/audiochroma/' + file, 'rb')))
                data = data.T

                model.fit(data)
                joblib.dump(model, 'storage/models/' + name + '.model')

                print(name + '.model is created.')

def runMidiThoughModels(midi):
    print('Run ' + midi + ' through all models.')
    midiChroma = pickle.load(open('storage/midichroma/' + midi, 'rb'))
    midiChroma = midiChroma.T

    path = 'storage/models'

    results = {}

    for file in os.listdir(path):
        if not os.path.isfile(path + '/' + file):
            continue

        name, ext = file.rsplit('.', 1)

        if ext == 'model':
            model = joblib.load('storage/models/' + file)
            results[name] = model.score(midiChroma)

    res_sorted = sorted(results.items(), key=operator.itemgetter(1), reverse=True)

    for index, (name, score) in enumerate(res_sorted):
        print(str(index + 1) + ': ' + name + ' (score : ' + str(score) + ')')

def runMidisThroughModels():
    path = 'storage/midichroma'

    for file in os.listdir(path):
        if not os.path.isfile(path + '/' + file):
            continue

        name, ext = file.rsplit('.', 1)

        if ext == 'vector':
            runMidiThoughModels(file)

if __name__ == '__main__':
    # Steps
    # 1. Synth all midi files
    synthMidiFiles()

    # 2. Create chroma vectors for all midis
    createMidiChromas()

    # 3. Create chroma vectors for all audios
    createAudioChromas()

    # Debug: store visualizations of chroma vectors
    visualizeChromaVectors()

    # 4. Create models from audio chroma vectors
    createModels()

    # 5. Run midi chroma vectors through these models
    runMidisThroughModels()

    # 6. ???
    # 7. Profit!

