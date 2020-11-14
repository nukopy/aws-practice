import json
from typing import Any, Dict, List

import fastavro


def read_json_lines(filepath: str) -> List[Dict[str, Any]]:
    with open(file=filepath, mode="r", encoding="utf-8") as fp_input:
        json_lines: List[str] = fp_input.readlines()
        json_lines: List[Dict[str, Any]] = [json.loads(line) for line in json_lines]

    return json_lines


def read_avro(filepath: str) -> List[Dict[str, Any]]:
    with open(file=filepath, mode="rb") as f:
        records = []
        for record in fastavro.reader(f):
            records.append(record)

    return records


def test_reading_avro():
    dir_output = "./output/"
    path_json_line = dir_output + "log"
    path_avro = dir_output + "log.avro"

    # read
    records_json_line = read_json_lines(filepath=path_json_line)
    records_avro = read_avro(filepath=path_avro)

    # test
    assert records_json_line == records_avro
