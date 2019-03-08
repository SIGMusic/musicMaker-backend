from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify

from services.chord_stats import getNextChord
from services.chord_notation_converter import convert

app = Flask(__name__)
api = Api(app)

class GetChordName(Resource):
    def get(self):


class NextChord(Resource):
    def get(self):
        midi_chord = request.args.getlist('chord')[0].split(',')

        return jsonify(getNextChord(convert(midi_chord), depth=None))

api.add_resource(NextChord, "/nextchord")

if __name__ == "__main__":
    app.run(debug=True)