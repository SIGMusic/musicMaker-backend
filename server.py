from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from pychord import note_to_chord
from services.note_to_name import note_to_name
from services.parser import get_all_data_key_irrespective

from services.chord_stats import chord_stats

app = Flask(__name__)
api = Api(app)

class GetChordName(Resource):
    """
    Creates an object that allows API calls to determine the name of the chord from MIDI numbers
    Up to 7 notes can be inputted

    API call is structeurd as /chordname?notes=arg1,arg2,...,arg7
    """
    def get(self):
        midi_chord = request.args.getlist('notes')[0].split(',')
        pychord_chord = note_to_chord([note_to_name(int(i)) for i in midi_chord])
        result_dict = {("chord_" + str(i)) : str(pychord_chord[i]) for i in range(len(pychord_chord))}

        return jsonify(result_dict)

class GetNextChord(Resource):
    """
    Creates an object that allows API calls to determine the next chord from an arbitrary lenght list of preivous chords

    API call is structured as /nextchord?chords=arg1,arg2,...,argn
    """
    def get(self):
        chords = request.args.getlist('chords')[0].split(',')

        analyzer = chord_stats(len(chords))
        analyzer.analyse_songs(get_all_data_key_irrespective("data/McGill-Billboard"))

        return jsonify(analyzer.get_next_chord(chords, depth=None))


api.add_resource(GetChordName, "/chordname")
api.add_resource(GetNextChord, "/nextchord")

if __name__ == "__main__":
    app.run(debug=True)