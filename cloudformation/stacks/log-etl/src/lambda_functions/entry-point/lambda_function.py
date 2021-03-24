import json


def lambda_handler(event, context):
    print({"TEST-MESSAGE": "This is a test maessage."})
    print(json.dumps(event))
