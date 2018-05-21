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


# The hop length used for generating an visualizing chroma vectors
hop_length = 2048

# Function used to syntesize not-yet-synthesized MIDI files
def synthMidiFiles():
    print("Checking if all MIDI files are synthesized...")

    # MIDI files directory
    path = 'storage/midifiles'

    # Create a FluidSynth entity
    fs = FluidSynth()

    # Store original stdout
    original = sys.stdout

    # Loop over files in the directory
    for file in os.listdir(path):

        # Skip entires that are not files
        if not os.path.isfile(path + '/' + file):
            continue

        # Split file in name and extension
        name, ext = file.rsplit('.', 1)

        # Only process .mid files
        if ext == 'mid':

            # Only process not-yet-synthesized files
            if not os.path.exists('storage/midisynth/' + name + '.wav'):

                # Show message
                print(name + " must still be synthesized")

                # Redirect stdout to log file
                sys.stdout = open('storage/synthlog/' + name + '.log', 'w')

                # Convert MIDI to audio
                fs.midi_to_audio(path + '/' + file, 'storage/midisynth/' + name + '.wav')

                # Restore stdout and print message
                sys.stdout = original
                print(name + ".wav is created.")


# Function to convert synthesized MIDI files to chroma vectors
def createMidiChromas():
    print("Checking if all MIDI files have Chroma vectors generated...")

    # Path to synthesized MIDIs
    path = 'storage/midisynth'

    # Loop over files
    for file in os.listdir(path):

        # Skip entries that are not files
        if not os.path.isfile(path + '/' + file):
            continue

        # Split name and extension of file
        name, ext = file.rsplit('.', 1)

        # Only process .wav files
        if ext == 'wav':

            # Only process files that have no chroma vectors calculated yet
            if not os.path.exists('storage/midichroma/' + name + '.vector'):

                # Print message
                print(name + " must still be converted to chroma vector")

                # Load the audio into librosa
                x, sr = librosa.load('storage/midisynth/' + name + '.wav')

                # Calculate and store the chromagram
                chromagram = librosa.feature.chroma_cqt(x, sr=sr, hop_length=hop_length)
                pickle.dump(chromagram, open('storage/midichroma/' + name + '.vector', 'wb'))

                # Print message
                print(name + ".vector is created.")


# Function to create chroma vectors for audio files
def createAudioChromas():
    print("Checking if all audio files have Chroma vectors generated...")

    # Path to audio files
    path = 'storage/audiofiles'

    # Loop over files
    for file in os.listdir(path):

        # Only process files
        if not os.path.isfile(path + '/' + file):
            continue

        # Split name and extension of file
        name, ext = file.rsplit('.', 1)

        # Only process .wav and .mp3 files
        if ext == 'wav' or ext == 'mp3':

            # Only process files without chroma vectors associated yet
            if not os.path.exists('storage/audiochroma/' + name + '.vector'):

                # Print message
                print(name + " must still be converted to chroma vector")

                # Load file in librosa
                x, sr = librosa.load('storage/audiofiles/' + file)

                # Calculate and store chromagram
                chromagram = librosa.feature.chroma_cqt(x, sr=sr, hop_length=hop_length)
                pickle.dump(chromagram, open('storage/audiochroma/' + name + '.vector', 'wb'))

                # Print message
                print(name + ".vector is created.")


# Function to store visualization of chroma vectors
def visualizeChromaVectors():

    # Loop over all midi-based chroma vectors
    print('Visualizing MIDI-based Chroma vectors')
    for file in os.listdir('storage/midichroma'):

        # Get name without extension
        name, _ = file.rsplit('.', 1)

        # Create and store visualization of chroma vector
        plt.figure(figsize=(15, 5))
        librosa.display.specshow(pickle.load(open('storage/midichroma/' + file, 'rb')), x_axis='time', y_axis='chroma', hop_length=hop_length, cmap='coolwarm')
        plt.savefig('storage/midichroma-visual/' + name + '.png')


    # Loop over all audio-based chroma vectors
    print('Visualizing audio-based Chroma vectors')
    for file in os.listdir('storage/audiochroma'):

        # Get name without extension
        name, _ = file.rsplit('.', 1)

        # Create and store visualization of chroma vector
        plt.figure(figsize=(15, 5))
        librosa.display.specshow(pickle.load(open('storage/audiochroma/' + file, 'rb')), x_axis='time', y_axis='chroma', hop_length=hop_length, cmap='coolwarm')
        plt.savefig('storage/audiochroma-visual/' + name + '.png')


# Function to create HMMs for audio-based chroma vectors
def createModels():
    print("Checking if all audio files have Hidden Markov Models generated...")

    # Directory where audio chromas are stored
    path = 'storage/audiochroma'

    # Loop over files
    for file in os.listdir(path):

        # Only process files
        if not os.path.isfile(path + '/' + file):
            continue

        # Split name and extension
        name, ext = file.rsplit('.', 1)

        # Only process .vector files
        if ext == 'vector':

            # Only process files that have no associated model yet
            if not os.path.exists('storage/models/' + name + '.model'):
                print(name + " has no associated model yet")

                # Create model
                model = hmm .GaussianHMM(n_components=5, covariance_type="full", n_iter=500, algorithm="map",transmat_prior=1.1)

                # Load data and transform from (features, samples) to (samples, features)
                data = np.array(pickle.load(open('storage/audiochroma/' + file, 'rb')))
                data = data.T

                # Train model to fit the data and store the model
                model.fit(data)
                joblib.dump(model, 'storage/models/' + name + '.model')

                # Print message
                print(name + '.model is created.')

# Function to run one MIDI files through all HMMs
def runMidiThoughModels(midi):

    # Load chroma vectors for this MIDI
    print('Run ' + midi + ' through all models.')
    midiChroma = pickle.load(open('storage/midichroma/' + midi, 'rb'))
    midiChroma = midiChroma.T

    # Path where the models are stored
    path = 'storage/models'

    # Store results for all models
    results = {}

    # Loop over models
    for file in os.listdir(path):
        if not os.path.isfile(path + '/' + file):
            continue

        # Split name and extension
        name, ext = file.rsplit('.', 1)

        # Only process models
        if ext == 'model':

            # Load model and score the MIDI chroma vector
            model = joblib.load('storage/models/' + file)
            results[name] = model.score(midiChroma)

    # Sort the scores so the best result is on top
    res_sorted = sorted(results.items(), key=operator.itemgetter(1), reverse=True)

    # Print the results
    for index, (name, score) in enumerate(res_sorted):
        print(str(index + 1) + ': ' + name + ' (score : ' + str(score) + ')')

# Function to run all MIDIs through all models
def runMidisThroughModels():

    # Path where the MIDI chroma respresentations are stored
    path = 'storage/midichroma'

    # Loop over MIDI representations
    for file in os.listdir(path):
        if not os.path.isfile(path + '/' + file):
            continue

        # Split name and extension
        name, ext = file.rsplit('.', 1)

        # Process .vector files
        if ext == 'vector':
            runMidiThoughModels(file)


# Main entry for the pipeline
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

