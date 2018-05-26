import pretty_midi
import os

def shift(file):
    data = pretty_midi.PrettyMIDI('storage/midifiles/' + file)

    name, ext = file.split('.', 1)

    if not os.path.exists('storage/midishifted/' + name):
        os.makedirs('storage/midishifted/' + name)

    data.write('storage/midishifted/' + name + '/' + name + '_0.mid')

    for x in range(1, 12):
        print(x)
        for instrument in data.instruments:
            # Don't want to shift drum notes
            if not instrument.is_drum:
                for note in instrument.notes:
                    note.pitch += 1
        data.write('storage/midishifted/' + name + '/' + name + '_' + str(x)  + '.mid')


if __name__ == '__main__':
    shift('Donna Summer - I Feel Love (version 1).mid')
