import random
import string

from app.aws.dynamodb import DynamoDB


db = DynamoDB()
# response = db.table.put_item(Item={"pet_id": "kuro", "shop_id": 2, "kind": "cat"})
SHOP_IDS = [i for i in range(1, 11)]
KINDS = ["bird", "cat", "dog"]
random.seed(111)


def create_random_pet():
    return {
        "pet_id": "".join(
            [random.choice(string.ascii_letters + string.digits) for _ in range(5)]
        ),
        "shop_id": random.choice(SHOP_IDS),
        "kind": random.choice(KINDS),
    }


def create_random_pets(n=50):
    return [create_random_pet() for _ in range(n)]


def put_pets(n=50):
    items = create_random_pets(n)
    db.batch_putting(items)


def update_pet(kind="PANDA"):
    keys = [
        {"pet_id": "1PFJn", "shop_id": 4},
        {"pet_id": "2znZP", "shop_id": 8},
        {"pet_id": "A7kFJ", "shop_id": 4},
    ]
    item = {"kind": kind}

    for key in keys:
        db.update_item(key=key, item=item)


def get_panda():
    items = db.scan()
    items_panda = [item for item in items if item["kind"] == "PANDA"]

    return items, items_panda


if __name__ == "__main__":
    # DynamoDB の更新のテスト
    # update_pet("HOGE")
    # update_pet("PANDA")
    # put_pets(n=50)
    pass
