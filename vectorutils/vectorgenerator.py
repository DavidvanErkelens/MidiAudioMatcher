#   VectorGenerator.py
#
#   Class that takes care of generating chroma vectors for existing audio files
#
#   Author: David van Erkelens <david.vanerkelens@student.uva.nl>


# Includes
import os
import librosa, librosa.display
import pickle

# Class definition
class VectorGenerator:

    # Class constructor
    def __init__(self, storage_path = 'storage', debug = True, force = False):
        self.storage_path = storage_path
        self.debug = debug
        self.force = force
        self.hop_length = 2048

        if self.debug:
            print('\n======================================= ')
            print('      Initializing VectorGenerator      ')
            print('======================================= ')


    def generateEverything(self):
        self.generateMidi()
        self.generateAudio()

    def generateMidi(self):

        # Format source path
        path = self.storage_path + '/midisynth'

        # Loop over files
        for file in os.listdir(path):

            # Try to generate chroma vectors if the path is a file
            if os.path.isfile(path + '/' + file):
                self.generateChroma('midi', file)

    def generateAudio(self):

        # Format source path
        path = self.storage_path + '/audiofiles'

        # Loop over files
        for file in os.listdir(path):

            # Try to generate chroma vectors if the path is a file
            if os.path.isfile(path + '/' + file):
                self.generateChroma('audio', file)


    def generateChroma(self, version, file):

        # Format source folder name depending on which version we're dealing with
        sourceFolder = 'audiofiles' if version == 'audio' else 'midisynth'
        
        # Format source path
        source = self.storage_path + '/' + sourceFolder + '/' + file

        # If the source does not exist, stop processing
        if not os.path.exists(source):
            return

        # Split filename in name and extension
        name, ext = file.rsplit('.', 1)

        # Only process .wav or .mp3 files
        if ext != 'wav' and ext != 'mp3':
            return

        # If we already have vectors and don't want to force new ones, stop
        if self.isGenerated(version, file) and not self.force:

            if self.debug:
                print('Chroma vectors for ' + file + ' are already generated.')

            return

        # Print debug statement if necessary
        if self.debug:
            print("Generating chroma vectors for " + file + " (" + version + ")...")

        # Format the target path
        target = self.storage_path + '/' + version + 'chroma/' + name + '.vector'

        # Load the audio into librosa
        x, sr = librosa.load(source)

        # Calculate and store the chromagram
        chromagram = librosa.feature.chroma_cqt(x, sr=sr, hop_length=self.hop_length)
        pickle.dump(chromagram, open(target, 'wb'))



    # Function to check if a certain set of chroma vectors has already been generated
    def isGenerated(self, version, file):

        # Get filename of the audio
        name, _ = file.rsplit('.', 1)

        # Check if the Chroma vectors for this file and version already exist
        return os.path.exists(self.storage_path + '/' + version + 'chroma/' + name + '.vector')
