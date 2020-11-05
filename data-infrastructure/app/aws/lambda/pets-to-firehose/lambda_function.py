import json

import utils
from firehose import Firehose


def filter_events(records, event_name: str = "INSERT"):
    return [rec for rec in records if rec["eventName"] == event_name]


def lambda_handler(event, context):
    # log
    print(event)

    # create Firehose client
    fh = Firehose()

    # process event
    records = event["Records"]
    records_for_fh = filter_events(records, event_name="INSERT")

    # transimit by record unit
    for rec in records_for_fh:
        fh.create_item({"Data": json.dumps(rec)})
        print(rec)


if __name__ == "__main__":
    # test
    event = utils.load_json("./event.json")
    lambda_handler(event, {})
