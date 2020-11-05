import json
from typing import Any, Dict, List

from boto3.dynamodb.types import TypeDeserializer

import utils
from firehose import Firehose


td = TypeDeserializer()


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


def lambda_handler(event, context):
    # log
    print(event)

    # create Firehose client
    fh = Firehose()

    # process event
    events = event["Records"]
    events = filter_events(events)
    new_images = extract_NewImage(events)
    records_dynamodb = deserialize_dynamodb_NewImages(new_images)

    # transimit by record unit
    for rec in records_dynamodb:
        fh.put_item({"Data": json.dumps(rec)})
        print(rec)


if __name__ == "__main__":
    # test
    event = utils.load_json("./event.json")
    lambda_handler(event, {})
