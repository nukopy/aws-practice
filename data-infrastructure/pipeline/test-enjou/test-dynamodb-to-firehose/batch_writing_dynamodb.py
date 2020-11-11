import random
import string

from app.aws.dynamodb import DynamoDB


db = DynamoDB()
CATEGORIES = [i for i in range(1, 11)]
random.seed(111)


def create_random_record():
    return {
        "id": "".join(
            [random.choice(string.ascii_letters + string.digits) for _ in range(5)]
        ),
        "category": random.choice(CATEGORIES),
    }


def create_random_records(n=10):
    return [create_random_record() for _ in range(n)]


def put_records(n=10):
    items = create_random_records(n)
    db.batch_putting(items)


if __name__ == "__main__":
    # DynamoDB の更新のテスト
    # update_record("HOGE")
    # update_record("PANDA")
    # put_records(n=50)
    pass
