from flask import Flask
from flask_restful import Resource, Api
from flask_jsonpify import jsonify

from services.dummy_function import get_chord_probabilities

app = Flask(__name__)
api = Api(app)

class NextChord(Resource):
    def get(self, chord):
        return jsonify(get_chord_probabilities(chord))

api.add_resource(NextChord, "/next/<chord>")

if __name__ == "__main__":
    app.run(debug=True)