import json
import importlib.resources as pkg_resources
from jsonschema import validate
from . import schema

class SchemaValidator:

    QUERY_BATCH_SCHEMA = "reconciliation-query-batch.json"
    RESULT_BATCH_SCHEMA = "reconciliation-result-batch.json"

    def __init__(self):
        #load schema files
        with pkg_resources.open_text(schema, self.QUERY_BATCH_SCHEMA) as f:
            self.query_batch_schema = json.load(f)
        with pkg_resources.open_text(schema, self.RESULT_BATCH_SCHEMA) as f:
            self.result_batch_schema = json.load(f)            

    def validate_query_batch(self, query_batch):
        """
        Validates a query batch agaist the query batch schema
        """
        validate(instance=query_batch, schema=self.query_batch_schema)
        return

    def validate_result_batch(self, result_batch):
        """
        Validates a result batch against the result batch schema
        """
        validate(instance=result_batch, schema=self.result_batch_schema)
        pass
