from pychord import Chord
from pychord import note_to_chord

from services.note_to_name import note_to_name

def convert(midi_chord):
    chord_notes = []

    for note in midi_chord:
        chord_notes.append(note_to_name(int(note)))

    ch = note_to_chord(chord_notes)[0]

    chord_name = ch._chord
    chord_root = ch._root
    chord_quality = ch._quality

    return str(ch)