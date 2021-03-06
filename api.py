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


class Reconciliation(MethodView):
    """
    Reconciliation endpoint, processes a query batch if provided and returns a
    reconciliation candidates batch, otherwhise returns the service manifest.
    """

    def _service_manifest(self):
        print("no queries, respond with manifest")
        manifest = load_manifest(MANIFEST_FILE)
        return jsonpify(manifest)
    
    def get(self):
        return self._service_manifest()

    def post(self):
        
        if "queries" in request.form:
            # process query batch
            print("queries recieved")
            queries = json.loads(request.form["queries"])
            validator.validate_query_batch(queries)

            results = unesco.query_batch(queries)
            validator.validate_result_batch(results)

            return jsonpify(results)
        
        else:
            # return service manifest
            return self._service_manifest()


class Preview(MethodView):
    """
    Endpoint for the preview service
    """

    def get(self, id_):
        preview = unesco.preview(id_)
        return make_response(preview)



if __name__ == "__main__":

    app.add_url_rule("/", view_func=Reconciliation.as_view("reconciliation"))
    app.add_url_rule("/preview/<string:id_>", view_func=Preview.as_view("preview"))

    app.run(host="0.0.0.0", debug=True)