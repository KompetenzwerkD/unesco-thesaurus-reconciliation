import json
import importlib.resources as pkg_resources
from jsonschema import validate

from . import schema
MANIFEST_SCHEMA = "manifest.json"


def load_manifest(filepath):
    """
    Loads service manifest file and validates it against the schema.
    """

    with pkg_resources.open_text(schema, MANIFEST_SCHEMA) as f:
        manifest_schema = json.load(f)
    
    with open(filepath) as f:
        manifest = json.load(f)

    validate(instance=manifest, schema=manifest_schema)

    return manifest