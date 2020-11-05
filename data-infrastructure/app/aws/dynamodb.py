import os
from typing import Any, Dict, List

from app.aws.base import Base


class DynamoDB(Base):
    def __init__(self):
        super().__init__("dynamodb")
        self.table_name = os.getenv("DYNAMODB_TABLE")
        self.table = self.client.Table(self.table_name)  # load table

    def create_item(self, item: Dict[str, Any]):
        self.table.put_item(item)

    def get_item(self, key: Dict[str, Any]) -> Dict[str, Any]:
        response = self.table.get_item(Key=key)
        item = response["item"]
        print("item:", item)
        return item

    def update_item(self, key: Dict[str, Any], item: Dict[str, Any]) -> None:
        # UpdateExpression
        update_expression = [
            f"{key} = :val{i}" for i, (key, _) in enumerate(item.items())
        ]
        str_update_expression = f"SET {', '.join(update_expression)}"

        # ExpressionAttributeValues
        expression_attribute = {
            f":val{i}": val for i, (_, val) in enumerate(item.items())
        }

        # update
        self.table.update_item(
            Key=key,
            UpdateExpression=str_update_expression,
            ExpressionAttributeValues=expression_attribute,
        )

    def delete_item(self, key: Dict[str, Any]) -> None:
        self.table.delete_item(Key=key)

    def batch_putting(self, items: List[Dict[str, Any]]) -> None:
        print("Start putting...")
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
        print("Done putting.")

    def get_table_list(self) -> List:
        table_list = self.client.tables.all()
        for table in table_list:
            print("table name:", table.table_name)

        return table_list


if __name__ == "__main__":
    db = DynamoDB()
