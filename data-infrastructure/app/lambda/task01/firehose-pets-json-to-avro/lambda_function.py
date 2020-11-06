import io
import json
import base64
from typing import Any, Dict, List

import fastavro


def create_payload(record) -> Dict[str, Any]:
    record_id = record["recordId"]
    ts = record["approximateArrivalTimestamp"]
    b64_data: str = record["data"]
    data = b64jsonstr_to_dict(b64_data)  # 更新後の DynamoDB のレコード

    # return {
    #     "recordId": record_id,
    #     "timestamp": ts,
    #     # "data": data,
    #     "data": data,
    #     "result": "Ok",  # MUST
    # }
    # DynamoDB のレコードのみ返すようにする

    return data


def load_json(path) -> Any:
    with open(path, mode="r", encoding="utf-8") as f:
        obj = json.load(f)
        return obj


def decode_b64str(b64str: str) -> bytes:
    return base64.b64decode(b64str)


def bytes_to_str(b: bytes) -> str:
    return b.decode("utf-8")


def b64jsonstr_to_dict(b64str: str) -> Dict[str, Any]:
    json_bytes = decode_b64str(b64str)
    json_str = bytes_to_str(json_bytes)
    return json.loads(json_str)


def payload_to_avro_binary(payload: List[Dict[str, Any]]):
    # load schema
    schema = fastavro.schema.load_schema("./record.avsc")

    # debug
    # with open("payload.json", "w") as f:
    #    json.dump(payload, f, indent=2)

    # write to iostream
    bytes_io = io.BytesIO()
    # fastavro.writer(fo=bytes_io, schema=schema, records=payload, codec="snappy")
    fastavro.writer(fo=bytes_io, schema=schema, records=payload)
    # with open("payload.avro", "wb") as f:
    #    fastavro.writer(fo=bytes_io, schema=schema, records=payload, codec="snappy")
    # with open("payload.avro", "rb") as f:
    #     bytes_ = f.read()

    return bytes_io.getvalue()


def lambda_handler(event, context):
    # log
    print("EVENT:\n", event)

    # process event
    records = event["records"]
    record_id = records[0]["recordId"]  # 1 つ以上の recordId を返さないと Firehose でエラーになる
    payloads = []

    for rec in records:
        payload = create_payload(rec)
        payloads.append(payload)

    print("PAYLOADS:\n", payloads)

    # Snappy 形式
    binary_payload = payload_to_avro_binary(payloads)

    # raise Exception
    b64_payload_bytes: bytes = base64.b64encode(binary_payload)
    b64_payload_str: str = b64_payload_bytes.decode("utf-8")
    # avro に戻す：base64.b64decode(b64_payload_str)
    print("PAYLOADS_BASE64_STR:\n", b64_payload_str)

    # create payload
    payload = [{"recordId": record_id, "data": b64_payload_str, "result": "Ok"}]
    print(payload)

    return {"records": payload}


if __name__ == "__main__":
    event = load_json("./event.json")
    response = lambda_handler(event, {})
    bytes_payload = response["records"]
