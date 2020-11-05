import json
import base64
from typing import Any, Dict


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


def lambda_handler(event, context):
    # log
    print("EVENT:\n", event)

    # process event
    records = event["records"]
    payload = []

    for rec in records:
        record_id = rec["recordId"]
        ts = rec["approximateArrivalTimestamp"]
        b64_data: str = rec["data"]
        data = b64jsonstr_to_dict(b64_data)
        payload.append(
            {
                "recordId": record_id,
                "timestamp": ts,
                # "data": data,
                "data": data,
                "ほげ": "ほげ",
                "result": "Ok",  # MUST
            }
        )
    print("PAYLOAD:", payload)

    return {"records": payload}


if __name__ == "__main__":
    event = load_json("./event.json")
    response = lambda_handler(event, {})
