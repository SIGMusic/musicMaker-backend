from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from pychord import note_to_chord

from services.chord_stats import getNextChord
from services.note_to_name import note_to_name

app = Flask(__name__)
api = Api(app)

class NextChord(Resource):
    def get(self):
        midi_chord = request.args.getlist('chord')[0].split(',')
        chord_notes = []

        for note in midi_chord:
            chord_notes.append(note_to_name(int(note)))

        chord = note_to_chord(chord_notes)

        return jsonify(getNextChord(str(chord[0]), depth=None))

api.add_resource(NextChord, "/nextchord")

if __name__ == "__main__":
    app.run(debug=True)