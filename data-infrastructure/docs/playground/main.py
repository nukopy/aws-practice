import avro.schema
import requests
from avro.datafile import DataFileWriter
from avro.io import DatumWriter

url = "http://www.mwsoft.jp/"
resp = requests.get(url)

with open("example.avsc", "rt") as avsc:
    schema = avro.schema.Parse(avsc.read())

with DataFileWriter(
    writer=open("contents.avro", "wb"),
    datum_writer=DatumWriter(),
    writer_schema=schema,
    codec="snappy",  # or "deflate"
) as writer:
    writer.append(
        {
            "url": url,
            "top_url": url,
            "header_encoding": requests.utils.get_encoding_from_headers(resp.headers),
            "contents": resp.content,
        }
    )
