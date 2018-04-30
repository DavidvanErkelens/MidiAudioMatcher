#   MidiSynth.py
#
#   File that takes care of syntesizing midi files

# Includes
import pretty_midi

def test():
    print("Test in MidiSynth")
    midi_data = pretty_midi.PrettyMIDI('Data/Queen.mid')
    # print(midi_data)
    audio_data = midi_data.fluidsynth(fs=22050)
    for x in audio_data:
        print(x)
    # print(audio_data)

