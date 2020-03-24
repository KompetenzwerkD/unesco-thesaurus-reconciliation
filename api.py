from flask import Flask, jsonify, make_response, request
from flask.views import MethodView
from flask_cors import CORS
import json

from reconciliation_api import load_manifest
from unesco_reconciliation import UnescoReconciliationService


MANIFEST_FILE = "manifest.json"

app = Flask(__name__)
CORS(app)

unesco = UnescoReconciliationService()


def jsonpify(data):
    if "callback" in request.args:
        cb = request.args["callback"]
        response = make_response("{}({})".format(cb, json.dumps(data)))
        response.mimetype = "text/javascript"
        return response
    else:
        return make_response(jsonify(data))


class Manifest(MethodView):
    def get(self):
        manifest = load_manifest(MANIFEST_FILE)
        return jsonpify(manifest)


class Query(MethodView):
    def get(self):
        query = request.args["query"]
        result = unesco.query(query)

        return jsonpify(result)


if __name__ == "__main__":

    app.add_url_rule("/", view_func=Manifest.as_view("manifest_view"))
    app.add_url_rule("/unesco", view_func=Query.as_view("query_view"))

    app.run(debug=True )