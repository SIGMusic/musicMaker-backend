from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from pychord import note_to_chord
from services.note_to_name import note_to_name

#from services.chord_stats import getNextChord
from services.dummy import dummy_func

app = Flask(__name__)
api = Api(app)

class GetChordName(Resource):
    def get(self):
        midi_chord = request.args.getlist('notes')[0].split(',')
        pychord_chord = note_to_chord([note_to_name(int(i)) for i in midi_chord])
        result_dict = {("chord_" + str(i)) : str(pychord_chord[i]) for i in range(len(pychord_chord))}

        return jsonify(result_dict)

class GetNextChord(Resource):
    def get(self):
        chords = request.args.getlist('chords')[0].split(',')

        return jsonify(dummy_func(chords, depth=None))


api.add_resource(GetChordName, "/chordname")
api.add_resource(GetNextChord, "/nextchord")

if __name__ == "__main__":
    app.run(debug=True)