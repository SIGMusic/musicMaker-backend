from audiolazy.lazy_midi import midi2str

def note_to_name(midi_number):
    full_name = midi2str(midi_number)
    return ''.join(l for l in full_name if not l.isdigit())