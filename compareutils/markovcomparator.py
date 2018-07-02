#   MarkovComparator.py
#
#   File that is able to compare MIDI files to audio files using the
#   Hidden Markov Model method
#
#   Author: David van Erkelens <david.vanerkelens@student.uva.nl>


# Includes
import os
import pickle
import hmmlearn
import operator
from sklearn.externals import joblib

# Class definition
class MarkovComparator:

    # Class constructor
    def __init__(self, storage_path = 'storage', debug = True, force = False):
        self.storage_path = storage_path
        self.debug = debug
        self.force = force

        if self.debug:
            print('\n======================================= ')
            print('     Initializing MarkovComparator      ')
            print('======================================= ')

    def compareToAll(self, midi):

        # Path to the models
        path = self.storage_path + '/models'

        # Make a list of all models
        audios = [x for x in os.listdir(path) if x.rsplit('.', 1)[1] == 'model']

        # Pass on to other function
        return self.compare(midi, audios)


    def compare(self, midi, audios):

        results = {}

        for audio in audios:
            results[audio] = self.compareOneAudio(midi, audio)

        # Sort the scores so the best result is on top
        res_sorted = sorted(results.items(), key=operator.itemgetter(1), reverse=True)

        # Return the best result
        return res_sorted[0]


    def compareOneAudio(self, midi, audio):

        # Get midi and audio file names
        midiName, _ = midi.rsplit('.', 1)
        audioName, _ = audio.rsplit('.', 1)

        # Format paths
        midiPath = self.storage_path + '/midichroma/' + midiName + '.vector'
        audioPath = self.storage_path + '/models/' + audioName + '.model'

        # Check if chroma vector exist
        if not os.path.exists(midiPath):
            print("WARNING: Cannot compare " + midiName + " since " + midiPath + " does not exist")
            return 0

        # Check if model exists
        if not os.path.exists(audioPath):
            print("WARNING: Cannot compare " + audioName + " since " + audioPath + " does not exist")
            return 0

        # Load the chroma vector of the midi
        midiChroma = pickle.load(open(midiPath, 'rb'))
        midiChroma = midiChroma.T

        # Load model and get score
        model = joblib.load(audioPath)
        return model.score(midiChroma)
