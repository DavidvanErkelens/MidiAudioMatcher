#   ModelGenerator.py
#
#   Class that takes care of generating hidden markov models for existing audio files
#
#   Author: David van Erkelens <david.vanerkelens@student.uva.nl>


# Includes
import os
from hmmlearn import hmm
from sklearn.externals import joblib
import numpy as np
import pickle

# Class definition
class ModelGenerator:

    # Class constructor
    def __init__(self, storage_path = 'storage', debug = True, force = False):
        self.storage_path = storage_path
        self.debug = debug
        self.force = force

        if self.debug:
            print('\n======================================= ')
            print('      Initializing ModelGenerator      ')
            print('======================================= ')


    def generateEverything(self):

        # Format source path
        path = self.storage_path + '/audiochroma'

        # Loop over files
        for file in os.listdir(path):

            # Try to generate chroma vectors if the path is a file
            if os.path.isfile(path + '/' + file):
                self.generateModel(file)


    def generateModel(self, file):

        # Format source path
        source = self.storage_path + '/audiochroma/' + file

        # Does this file exist?
        if not os.path.exists(source):

            # Print debug statement
            if self.debug:
                print("Trying to generate model for non-existing file " + file)

            return

        # Split filename in file and extension
        name, ext = file.rsplit('.', 1)

        # Only process vector files
        if ext != 'vector':
            return

        # Do we already have a model and shouldn't we overwrite it?
        if self.isGenerated(file) and not self.force:

            # Print debug statement
            if self.debug:
                print("Model for " + file + " is already generated")

            return

        # Print debug statement
        if self.debug:
            print ("Generating model for " + file)

        # Create model
        model = hmm.GaussianHMM(n_components=5, covariance_type="full", n_iter=500, algorithm="map",transmat_prior=1.1)

        # Load data and transform from (features, samples) to (samples, features)
        data = np.array(pickle.load(open(source, 'rb')))
        data = data.T

        # Format target path
        target = self.storage_path + '/models/' + name + '.model'

        # Train model to fit the data and store the model
        model.fit(data)
        joblib.dump(model, target)


    # Function to check if a certain model has already been generated
    def isGenerated(self, file):

        # Get filename of the audio
        name, _ = file.rsplit('.', 1)

        # Check if the Chroma vectors for this file and version already exist
        return os.path.exists(self.storage_path + '/' + 'models/' + name + '.model')
