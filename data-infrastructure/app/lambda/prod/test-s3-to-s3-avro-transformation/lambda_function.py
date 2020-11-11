import json
import uuid
from typing import Any, Dict, List
from urllib.parse import unquote_plus

import fastavro

from s3 import S3


SUFFIX = "avro"
s3_client = S3()


def load_json_lines(filepath: str) -> List[Dict[str, Any]]:
    with open(file=filepath, mode="r", encoding="utf-8") as fp_input:
        json_lines: List[str] = fp_input.readlines()
        json_lines: List[Dict[str, Any]] = [json.loads(line) for line in json_lines]

    return json_lines


def convert_avro(
    schema_path: str, records: List[Dict[str, Any]], filepath: str
) -> None:
    # load Avro schema
    schema = fastavro.schema.load_schema(schema_path)

    # convert records to Avro
    if ".avro" not in filepath:
        filepath = filepath + ".avro"

    with open(file=filepath, mode="wb") as fp_output:
        # TODO: codec を snappy にしたい．Lambda 上で Snappy を動かせなかった．
        fastavro.writer(fo=fp_output, schema=schema, records=records)
        # fastavro.writer(fo=fp_output, schema=schema, records=json_lines, codec="snappy")


def convert_logs_to_avro(input_path: str, output_path: str) -> None:
    """ convert a log file whose format is JSON-line into Avro format file """

    # load log file whose format is JSON-line
    json_lines = load_json_lines(input_path)

    # convert JSON-line to Avro format
    convert_avro(schema_path="./record.avsc", records=json_lines, filepath=output_path)


def read_avro(filepath: str = "output/sample-log.avro") -> List[Dict[str, Any]]:
    with open(file=filepath, mode="rb") as f:
        records = []
        for record in fastavro.reader(f):
            records.append(record)

    return records


def lambda_handler(event, context):
    print(json.dumps(event))

    # convert JSON-line format logs to Avro format file
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        target_bucket = "{}-{}".format(bucket, SUFFIX)
        key = unquote_plus(record["s3"]["object"]["key"])  # S3 object name

        # create path
        tmpkey = key.replace("/", "")
        download_path = "/tmp/{}{}".format(uuid.uuid4(), tmpkey)
        upload_path = "/tmp/{}-{}.avro".format(SUFFIX, tmpkey)
        s3_object_name = key + ".avro"

        # download file from S3
        s3_client.download_file(bucket=bucket, key=key, download_path=download_path)

        # convert to avro
        convert_logs_to_avro(input_path=download_path, output_path=upload_path)

        # upload Avro file to S3
        s3_client.upload_file(
            upload_path=upload_path, bucket=target_bucket, key=s3_object_name
        )


if __name__ == "__main__":
    # print("===== Converting to Avro format... =====")
    # convert_logs_to_avro(
    #     input_path="./input/sample-log", output_path="./output/sample-log.avro"
    # )

    print("===== Read Avro format =====")
    path = "./output/test-enjou-cloudwatch-logs-to-s3-7-2020-11-11-09-37-51-8fa81d73-e657-44d7-9fb3-555198e92570.avro"
    records = read_avro(path)
    print(records)
