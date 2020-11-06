import json
import logging
from typing import Any, Function, Dict, List

from boto3.dynamodb.types import TypeDeserializer

from firehose import Firehose

logger = logging.getLogger()
logger.setLevel(logging.INFO)

td = TypeDeserializer()


def func_logger(func: Function):
    def _inner(event, context):
        logger.info("===== Start function =====")
        logger.info(f"Recieved event: {json.dumps(event, indent=2)}")
        func(event, context)
        logger.info("===== End function =====")

    return _inner


def load_json(path) -> List[List[str]]:
    with open(path, mode="r", encoding="utf-8") as f:
        obj = json.load(f)
        return obj


def filter_events(records) -> List[Any]:
    filtered_records = [rec for rec in records if "NewImage" in rec["dynamodb"]]
    return filtered_records


def extract_NewImage(records) -> List[Any]:
    new_images = [rec["dynamodb"]["NewImage"] for rec in records]
    return new_images


def deserialize_dynamodb_NewImage(new_image: Dict[str, Any]) -> Dict[str, Any]:
    res = {}
    for key, val in new_image.items():
        if "N" in val:
            res[key] = int(td.deserialize(val))
        else:
            res[key] = td.deserialize(val)

    return res


def deserialize_dynamodb_NewImages(new_images: List[Any]) -> List[Any]:
    new_images = [deserialize_dynamodb_NewImage(record) for record in new_images]
    return new_images


@func_logger
def lambda_handler(event, context):
    # create Firehose client
    fh = Firehose()

    # process event
    events_dynamodb_update = event["Records"]  # see `event.json`
    events_dynamodb_update = filter_events(events_dynamodb_update)
    new_images = extract_NewImage(events_dynamodb_update)
    records_dynamodb = deserialize_dynamodb_NewImages(new_images)

    # transimit by record unit
    for rec in records_dynamodb:
        fh.put_item({"Data": json.dumps(rec)})

    logger.info(f"Sent to Firehose: {json.dumps(records_dynamodb, indent=2)}")


if __name__ == "__main__":
    # test
    event = load_json("./event.json")
    lambda_handler(event, {})
