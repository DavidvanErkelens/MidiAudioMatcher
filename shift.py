import pretty_midi

def shift():
    data = pretty_midi.PrettyMIDI('storage/midifiles/Donna Summer - I Feel Love (version 1).mid')
    for instrument in data.instruments:
        # Don't want to shift drum notes
        if not instrument.is_drum:
            for note in instrument.notes:
                note.pitch += 1

    data.write('storage/midishifted/love.mid')


if __name__ == '__main__':
    shift()
