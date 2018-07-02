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

    synth = MidiSynthesizer(storage, debug)
    synth.synthEverything()

    vec = VectorGenerator(storage, debug)
    vec.generateEverything()

    model = ModelGenerator(storage, debug)
    model.generateEverything()

    compare = 'BohemianRhapsody.mid'

    markov = MarkovComparator(storage, debug)
    start_time = time.time()
    print(markov.compareToAll(compare))
    end_time = time.time()
    total_time = end_time - start_time
    print("Running time for HMM: " + str(total_time))


    timewarp = TimeWarpComparator(storage, debug)
    start_time = time.time()
    print(timewarp.compareToAll(compare))
    end_time = time.time()
    total_time = end_time - start_time
    print("Running time for DTW: " + str(total_time))


if __name__ == '__main__':
    main()


