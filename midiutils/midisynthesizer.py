#   MidiSynthesizer.py
#
#   File that contains a class used when synthesizing MIDI files
#
#   Author: David van Erkelens <david.vanerkelens@student.uva.nl>


# Includes
import os
from midi2audio import FluidSynth

# Class definition
class MidiSynthesizer:

    # Class constructor
    def __init__(self, storage_path = 'storage', debug = True, force = False):
        self.storage_path = storage_path
        self.debug = debug
        self.force = force

        if self.debug:
            print('======================================= ')
            print('      Initializing MidiSynthesizer      ')
            print('======================================= ')


    # Function to synthesize all available MIDI files
    def synthEverything(self):
        path = self.storage_path + '/midifiles'

        for file in os.listdir(path):
            # Skip entires that are not files
            if not os.path.isfile(path + '/' + file):
                continue

            # Try to synthesize
            self.synthMidi(file)


    # Function to synthesize one MIDI file
    def synthMidi(self, midiFile):

        # Check if the file exists
        if not os.path.exists(self.storage_path + '/midifiles/' + midiFile):

            if self.debug:
                print("Trying to synthesize non-existing file " + midiFile)

            return

        # Is this file already synthesized (and do we not want to force a resynth)?
        if self.isSynthesized(midiFile) and not self.force:

            if self.debug:
                print(midiFile + " has already been synthesized.")

            return

        # Split the MIDI filename in parts
        name, ext = midiFile.rsplit('.', 1)

        # Is this a MIDI file?
        if ext != 'mid':
            return

        # We need FluidSynth
        fs = FluidSynth()

        # Synthesize MIDI file
        fs.midi_to_audio(self.storage_path + '/midifiles/' + midiFile, self.storage_path + '/midisynth/' + name + '.wav')

        # Print output if necessary
        if self.debug:
            print(midiFile + " has been synthesized.")


    # Returns a boolean to indicate if a midi file has already been synthesized
    def isSynthesized(self, midiFile):

        # Split the MIDI filename in parts
        name, _ = midiFile.rsplit('.', 1)

        # Does the synthesized file already exist?
        return os.path.exists(self.storage_path + '/midisynth/' + name + '.wav')
