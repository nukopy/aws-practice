import os
from typing import Any, Dict, List

from base import Base


class Firehose(Base):
    def __init__(self):
        super().__init__("firehose")
        self.firehose_stream = os.getenv("KINESIS_FIREHOSE_STREAM")

    def put_item(self, record: Dict[str, Any]) -> None:
        self.client.put_record(DeliveryStreamName=self.firehose_stream, Record=record)

    def batch_putting(self, records: List[Dict[str, Any]]) -> None:
        print("Start putting.")
        for rec in records:
            self.create_item(rec)
        print("Done putting.")

    def describe_stream(self) -> Dict[str, Any]:
        # describe "DeliveryStream"
        description = self.client.describe_delivery_stream(
            DeliveryStreamName=self.firehose_stream
        )
        return description


if __name__ == "__main__":
    fh = Firehose()

    # 配信ストリームの設定を出力
    fh.client.describe_delivery_stream(DeliveryStreamName="pets")
