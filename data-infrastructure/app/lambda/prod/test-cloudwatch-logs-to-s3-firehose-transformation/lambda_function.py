import base64
import json
import logging
from typing import Any, Callable, Dict, List


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def func_logger(func: Callable):
    def _inner(event, context):
        logger.info("===== Start function =====")
        logger.info(f"Recieved event: {json.dumps(event, indent=2)}")
        res = func(event, context)
        logger.info("===== End function =====")

        return res

    return _inner


def load_json(path) -> List[List[str]]:
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


def create_payload(record) -> Dict[str, Any]:
    record_id = record["recordId"]
    ts = record["approximateArrivalTimestamp"]
    b64_data: str = record["data"]
    data = b64jsonstr_to_dict(b64_data)  # 更新後の DynamoDB のレコード

    return {
        "recordId": record_id,
        "timestamp": ts,
        # "data": data,
        "data": data,
        "result": "Ok",  # MUST
    }


@func_logger
def lambda_handler(event, context):
    # process event
    records = event["records"]
    payloads = []

    for rec in records:
        payload = create_payload(rec)
        payloads.append(payload)

    return {"records": payloads}


if __name__ == "__main__":
    # test
    event = load_json("./event.json")
    res = lambda_handler(event, {})
