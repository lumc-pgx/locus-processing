import json

from locus_processing.schemas import LocusSchema
from marshmallow_jsonschema import JSONSchema

l = LocusSchema()
j = JSONSchema()
js = j.dump(l)
print(json.dumps(js.data, indent=4))
