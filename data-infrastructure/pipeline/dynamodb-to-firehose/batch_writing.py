import random
import string

from aws.dynamodb import DynamoDB


dynamodb = DynamoDB()
random.seed(111)


def create_random_record():
    return {
        "id": "".join(
            [random.choice(string.ascii_letters + string.digits)
             for _ in range(5)]
        ),
        "test_id": "".join(
            [random.choice(string.ascii_letters + string.digits)
             for _ in range(10)]
        )
    }


def create_random_records(n=50):
    return [create_random_record() for _ in range(n)]


def put_records(n=50):
    items = create_random_records(n)
    dynamodb
    dynamodb.batch_putting(items)


if __name__ == "__main__":
    # DynamoDB の更新のテスト
    # update_pet("HOGE")
    # update_pet("PANDA")
    # put_records(n=50)
    pass
