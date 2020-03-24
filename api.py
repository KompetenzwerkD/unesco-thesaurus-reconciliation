from flask import Flask, jsonify, make_response, request
from flask.views import MethodView
from flask_cors import CORS
import json

from reconciliation_api import load_manifest, SchemaValidator
from unesco_reconciliation import UnescoReconciliationService


MANIFEST_FILE = "manifest.json"

app = Flask(__name__)
CORS(app)

unesco = UnescoReconciliationService()
validator = SchemaValidator()

def jsonpify(data):
    """
    Returns response as jsonp if callback is set in arguments.
    If not, return normal json response.
    """
    if "callback" in request.args:
        print("callback")
        cb = request.args["callback"]
        response = make_response("{}({})".format(cb, json.dumps(data)))
        response.mimetype = "text/javascript"
        return response
    else:
        return make_response(jsonify(data))


class Manifest(MethodView):
    def post(self):

        if "queries" in request.form:
            print("queries recieved")
            queries = json.loads(request.form["queries"])
            validator.validate_query_batch(queries)

            results = unesco.query_batch(queries)
            validator.validate_result_batch(results)

            return jsonpify(results)

        else:
            print("no queries, respond with manifest")
            manifest = load_manifest(MANIFEST_FILE)
            return jsonpify(manifest)


class Query(MethodView):
    def get(self):
        query = request.args["query"]
        result = unesco.query(query)

        return jsonpify(result)


if __name__ == "__main__":

    app.add_url_rule("/", view_func=Manifest.as_view("manifest_view"))
    app.add_url_rule("/reconsile", view_func=Query.as_view("query_view"))

    app.run(host="0.0.0.0", debug=True)