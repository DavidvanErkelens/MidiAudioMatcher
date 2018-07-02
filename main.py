# Imports
from midiutils.midisynthesizer import MidiSynthesizer
from vectorutils.vectorgenerator import VectorGenerator
from pipelineutils.modelgenerator import ModelGenerator
from pipelineutils.comparator import Comparator
from compareutils.markovcomparator import MarkovComparator
from compareutils.timewarpcomparator import TimeWarpComparator

import time

def main():
    # Variables
    debug = True
    storage = 'storage'


    # synth = MidiSynthesizer(storage, debug)
    # synth.synthEverything()

    # vec = VectorGenerator(storage, debug)
    # vec.generateEverything()

    # model = ModelGenerator(storage, debug)
    # model.generateEverything()

    start_time = time.time()

    timewarp = TimeWarpComparator(storage, debug)
    # comparator = Comparator(markov)
    # markov.compare('BohemianRhapsody.mid', ['07 - Rock Me.mp3','bohemian-rhapsody.mp3'])
    print(timewarp.compareToAll('BohemianRhapsody.mid'))

    end_time = time.time()


if __name__ == '__main__':
    main()


