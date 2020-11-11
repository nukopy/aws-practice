import json

import avro.schema
import fastavro

with open("./record-copy.avsc", "r") as fp:
    schema = json.load(fp)

with open("./payload.json", "r") as fp:
    payload = json.load(fp)


fastavro.validate(datum=payload[0], schema=schema)
avro.schema.SchemaFromJSONData(schema)
