import os
import boto3


class Base:
    SERVICES = ["firehose", "s3"]

    def __init__(self, service: str):
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region = os.getenv("AWS_REGION")

        # client
        if service in self.SERVICES:
            self.client = boto3.client(
                service,
                # aws_access_key_id=self.access_key,
                # aws_secret_access_key=self.secret_key,
                # region_name=self.region,
            )
        else:
            self.client = boto3.resource(
                service,
                # aws_access_key_id=self.access_key,
                # aws_secret_access_key=self.secret_key,
                # region_name=self.region,
            )
