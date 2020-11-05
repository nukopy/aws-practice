# 認証情報について

- Lambda にデプロイした関数では，`boto3` に認証情報（アクセスキー ID，アクセスシークレットキー）を渡さなくても，勝手に AWS アカウントに紐づくそれらを読み込み，boto3 を扱える．

ローカル

```py
class Base:
    def __init__(self, service: str):
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region = os.getenv("AWS_REGION")

        # client
        if service == "firehose":
            self.client = boto3.client(
                service,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
            )
        else:
            self.client = boto3.resource(
                service,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
            )
```

AWS 上

```py
class Base:
    def __init__(self, service: str):
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region = os.getenv("AWS_REGION")

        # client
        if service == "firehose":
            self.client = boto3.client(
                service,
                # FIXME: ここをコメントアウトすると動く！
                # aws_access_key_id=self.access_key,
                # aws_secret_access_key=self.secret_key,
                region_name=self.region,
            )
        else:
            self.client = boto3.resource(
                service,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
            )
```

認証情報を渡すと以下のようなエラーが出る．

```sh
[ERROR] ClientError: An error occurred (UnrecognizedClientException) when calling the DescribeDeliveryStream operation: The security token included in the request is invalid.
Traceback (most recent call last):
  File "/var/task/lambda_function.py", line 18, in lambda_handler
    fh.describe_stream()
  File "/var/task/firehose.py", line 23, in describe_stream
    self.client.describe_delivery_stream(DeliveryStreamName=self.firehose_stream)
  File "/var/runtime/botocore/client.py", line 316, in _api_call
    return self._make_api_call(operation_name, kwargs)
  File "/var/runtime/botocore/client.py", line 635, in _make_api_call
    raise error_class(parsed_response, operation_name)
```
