from typing import Any, Dict, List

from base import Base


class Firehose(Base):
    def __init__(self):
        super().__init__("firehose")

    def put_item(self, record: Dict[str, Any]):
        self.client.put_record(DeliveryStreamName=self.firehose_stream, Record=record)

    def batch_putting(self, records: List[Dict[str, Any]]) -> None:
        print("Start putting.")
        for rec in records:
            self.put_item(rec)
        print("Done putting.")


if __name__ == "__main__":
    stream = Firehose()
