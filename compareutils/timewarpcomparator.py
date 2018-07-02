#   TimeWarpComparator.py
#
#   File that is able to compare MIDI files to audio files using the
#   Dynamic Time Warping method
#
#   Author: David van Erkelens <david.vanerkelens@student.uva.nl>


# Includes
import os
import pickle
import operator
import numpy as np
from dtw import dtw 
import time

# Class definition
class TimeWarpComparator:

    # Class constructor
    def __init__(self, storage_path = 'storage', debug = True, force = False):
        self.storage_path = storage_path
        self.debug = debug
        self.force = force

        if self.debug:
            print('\n======================================= ')
            print('    Initializing TimeWarpComparator      ')
            print('======================================= ')

    def compareToAll(self, midi):

        # Path to the audio chromas
        path = self.storage_path + '/audiochroma'

        # Make a list of all models
        audios = [x for x in os.listdir(path) if x.rsplit('.', 1)[1] == 'vector']

        # Pass on to other function
        return self.compare(midi, audios)


    def compare(self, midi, audios):

        results = {}

        for audio in audios:
            start_time = time.time()
            results[audio] = self.compareOneAudio(midi, audio)
            end_time = time.time()
            total_time = end_time - start_time
            print("Time for one comparison: " + str(total_time))
            # print(results)

        # Sort the scores so the best result is on top (not reverse, since the
        # score returned is a distance, so a lower score is better)
        res_sorted = sorted(results.items(), key=operator.itemgetter(1))

        # Return the best result
        return res_sorted[0]


    def compareOneAudio(self, midi, audio):

        # Get midi and audio file names
        midiName, _ = midi.rsplit('.', 1)
        audioName, _ = audio.rsplit('.', 1)

        # Format paths
        midiPath = self.storage_path + '/midichroma/' + midiName + '.vector'
        audioPath = self.storage_path + '/audiochroma/' + audioName + '.vector'

        # Check if chroma vector exist
        if not os.path.exists(midiPath):
            print("WARNING: Cannot compare " + midiName + " since " + midiPath + " does not exist")
            return 0

        # Check if model exists
        if not os.path.exists(audioPath):
            print("WARNING: Cannot compare " + audioName + " since " + audioPath + " does not exist")
            return 0

        # Load the chroma vectors of the midi and audio
        midiChroma = pickle.load(open(midiPath, 'rb'))
        audioChroma = pickle.load(open(audioPath, 'rb'))

        # Calculate distance
        distance, _, _, _ = dtw(midiChroma.T, audioChroma.T, dist=lambda x, y: np.linalg.norm(x - y, ord=1))
        return distance
