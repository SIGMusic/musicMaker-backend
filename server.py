from flask import Flask
from flask_restful import Resource, Api
from flask_jsonpify import jsonify

from services.chord_stats import getNextChord

app = Flask(__name__)
api = Api(app)

class NextChord(Resource):
    def get(self, chord):
        return jsonify(getNextChord([chord], depth=None))

api.add_resource(NextChord, "/next/<chord>")

if __name__ == "__main__":
    app.run(debug=True)