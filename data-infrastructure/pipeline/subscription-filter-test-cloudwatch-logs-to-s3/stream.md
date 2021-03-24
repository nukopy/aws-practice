# AWS で作るパイプライン

## DynamoDB の更新 -> Lambda 発火 -> Firehose へ更新したレコードを投げる -> S3 へ保存

1. テーブルの作成：DynamoDB にテーブルを作る
2. Lambda 関数の作成：Lambda のコンソールから新規関数の作成（DynamoDB ストリームを読むための IAM ロールの設定などに気を付ける）
3. トリガーの追加：作成した関数のコンソールへ行き，"設定" タブの "トリガーを追加" をクリックすると，どのサービスをトリガーにするのか選択できるため，DynamoDB を選択し，1 で作成したテーブルを選択する．
4. これで DynamoDB の更新をトリガーに Lambda が発火するようになる
5. Lambda 関数のテスト：送られてくるイベントを `print(event)` する関数を実装し，一度 DynamoDB にレコードを追加する．Lambda の CloudWatch Logs のログを確認し，`event` オブジェクトに更新されたレコードの情報がちゃんと入っているか（トリガーの設定が上手くいっているか）を確認する．また，ここでの `event` の出力を `event.json` としてローカルやブラウザ上のテスト用に保存しておくと良い．
6. テストするときに，Lambda にデプロイした実装で `boto3` の `client` をインスタンス化するときに，AWS の認証情報を渡すとクライアントが上手く動作しないので注意．つまり，Lambda から他のサービスに boto3 でアクセスする際は認証情報は必要ない（AWS 側でよしなにやってくれてる．そのコンソールからテスト実行する時点で認証できてるようなもんだもんね．）．

## CloudWatch Logs の更新 -> Lambda 発火 -> Firehose へ更新したレコードを投げる -> S3 へ保存

1. Lambda 関数の作成：Lambda のコンソールから新規関数の作成（IAM ロールの設定などに気を付ける）
2. ロググループの作成：これは 1 の時点でその関数に紐づくロググループ `/aws/lambda/[関数名]` が自動で作成される
3. Lambda のコンソールからテストを行い，`print(event)` を実行したときにロググループにちゃんとログが吐かれるかテストする
4. ロググループのログの更新でで発火される Lambda 関数の作成

---

## CloudWatch Logs サブスクリプションフィルタの使用

- 参考
  - 公式 doc：[CloudWatch Logs サブスクリプションフィルタの使用](https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/logs/SubscriptionFilters.html)
  - classmethod：[]()

Lambda Function などで作り込みを行わず，CloudWatch Logs のログデータを S3 に出力するには，Kinesis Data Firehose が利用できる．

ここでは，Kinesis Data Firehose を介して，CloudWatch Logs のデータを S3 へ出力する設定を紹介する．CloudWatch Logs から Kinesis Data Firehose へ出力するには，CloudWatch Logs の**サブスクリプションフィルタ**の設定が必要になるが，この設定はマネジメントコンソールでは行えないため，関連する作業含め AWS CLI を利用して設定を行う．

### 事前準備

- 環境変数の設定
  - `$CWL_LOG_GROUP_NAME`
  - `$KINESIS_FIREHOSE_ARN`
  - `$CWL_ROLE_ARN`：CloudWatch Logs が Kinesis Data Firehose 配信ストリームへ出力する IAM ロールの ARN
- [x] S3 バケット作成
- [x] Kinesis Data Firehose 用の IAM ロールの作成
- [x] ロググループの作成
  - Lambda で関数の作成を行うと勝手にできる
- [x] 配信ストリームの作成
- [x] CloudWatch Logs 用の IAM ロールの作成

### サブスクリプションフィルタの設定

- 目的
  - CloudWatch Logs に出力されたログを Firehose 経由で S3 に吐き出す流れの自動化．それがサブスクリプションフィルタ．
- [Amazon Kinesis Data Firehose のサブスクリプションフィルタ](https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/logs/SubscriptionFilters.html#FirehoseExample)
  - **必ずドキュメントを見ろ．適当な推測で設定を行うな．**

#### 1. S3 バケットの作成

まず，S3 にバケットを作成．CloudWatch Logs 専用に作成することを推奨．

- IAM ロールを作成して，Amazon Kinesis Data Firehose に Amazon S3 バケットにデータを置く権限を付与する．
  - 詳細については，『Amazon Kinesis Data Firehose 開発者ガイド』の「Amazon Kinesis Data Firehose を使用したユーザーアクセスの制御」を参照してください。
  - まず，テキストエディタを使用して次のようにファイル `TrustPolicyForFirehose.json` で信頼ポリシーを作成する．[account-id] は，AWS アカウント ID で置き換える．

```json
{
  "Statement": {
    "Effect": "Allow",
    "Principal": { "Service": "firehose.amazonaws.com" },
    "Action": "sts:AssumeRole",
    "Condition": { "StringEquals": { "sts:ExternalId": "[account-id]" } }
  }
}
```

#### 2. IAM ロール，関連付けるポリシーの作成：Firehose to S3

- `create-role` コマンドを使用し，信頼ポリシーファイルを指定して IAM ロールを作成する
  - 後のステップで必要になるため，返された Role.Arn 値を書き留める

```sh
aws iam create-role --role-name firehose-to-s3 --assume-role-policy-document file://./TrustPolicyForCWL.json
```

- 権限ポリシーを作成し，Kinesis Data Firehose がアカウントで実行できるアクションを定義する
  - まず，ファイル（`PermissionsForFirehose.json` など）権限ポリシーを作成する．テキストエディタを使用してこのポリシーを作成する．

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:AbortMultipartUpload",
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads",
        "s3:PutObject"
      ],
      "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"]
    }
  ]
}
```

- 次の `put-role-policy` コマンドを使用し，アクセス許可ポリシーをロールに関連付ける

```sh
aws iam put-role-policy  --role-name firehose-to-s3 --policy-name firehose-to-s3 --policy-document file://./PermissionsForFirehose.json
```

#### 3. Kinesis Data Firehose 配信ストリームの作成

- 次のように，送信先 Kinesis Data Firehose 配信ストリームを作成する．2 で作成した IAM ロールの RoleARN と，1 で作成した S3 バケットの BucketARN のプレースホルダー値を，作成したロールおよびバケット ARN に置き換える．

```sh
aws firehose create-delivery-stream \
   --delivery-stream-name "${KINESIS_FIREHOSE_STREAM}" \
   --s3-destination-configuration \
  '{"RoleARN": "arn:aws:iam::489089015667:role/firehose-to-s3", "BucketARN": "arn:aws:s3:::test-cloudwatch-logs-to-s3"}'

# 出力
{
    "DeliveryStreamARN": "arn:aws:firehose:ap-northeast-1:489089015667:deliverystream/test-cloudwatch-logs-to-s3"
}
```

Kinesis Data Firehose は，Amazon S3 オブジェクトに提供された `YYYY/MM/DD/HH` UTC 時間形式をプレフィックスで自動的に使用することに注意．時間形式プレフィックスの前に，追加のプレフィックスを指定できる．プレフィックスの最後がフォワードスラッシュ（`/`），の場合は，Amazon S3 バケット内のフォルダとして表示される．

- ストリームがアクティブになるまで待つ（これには数分かかる可能性がある）
  - Kinesis Data Firehose `describe-delivery-stream` コマンドを使用し，`DeliveryStreamDescription.DeliveryStreamStatus` プロパティをチェックできる．
  - さらに，後のステップで必要になるため，`DeliveryStreamDescription.DeliveryStreamARN` 値を書き留める．
  - コンソールに行き，デバッグ用に `Buffer size` と `Buffer interval` の設定を最小に変更する

```sh
aws firehose describe-delivery-stream --delivery-stream-name "${KINESIS_FIREHOSE_STREAM}"

# 出力
{
    "DeliveryStreamDescription": {
        "DeliveryStreamName": "test-cloudwatch-logs-to-s3",
        "DeliveryStreamARN": "arn:aws:firehose:ap-northeast-1:489089015667:deliverystream/test-cloudwatch-logs-to-s3",
        "DeliveryStreamStatus": "ACTIVE",
        "DeliveryStreamEncryptionConfiguration": {
            "Status": "DISABLED"
        },
        "DeliveryStreamType": "DirectPut",
        "VersionId": "2",
        "CreateTimestamp": "2020-11-06T13:14:06.059000+09:00",
        "LastUpdateTimestamp": "2020-11-06T13:19:30.259000+09:00",
        "Destinations": [
            {
                "DestinationId": "destinationId-000000000001",
                "S3DestinationDescription": {
                    "RoleARN": "arn:aws:iam::489089015667:role/firehose-to-s3",
                    "BucketARN": "arn:aws:s3:::test-cloudwatch-logs-to-s3",
                    "Prefix": "",
                    "ErrorOutputPrefix": "",
                    "BufferingHints": {
                        "SizeInMBs": 1,
                        "IntervalInSeconds": 60
                    },
                    "CompressionFormat": "UNCOMPRESSED",
                    "EncryptionConfiguration": {
                        "NoEncryptionConfig": "NoEncryption"
                    },
                    "CloudWatchLoggingOptions": {
                        "Enabled": false
                    }
                },
                "ExtendedS3DestinationDescription": {
                    "RoleARN": "arn:aws:iam::489089015667:role/firehose-to-s3",
                    "BucketARN": "arn:aws:s3:::test-cloudwatch-logs-to-s3",
                    "Prefix": "",
                    "ErrorOutputPrefix": "",
                    "BufferingHints": {
                        "SizeInMBs": 1,
                        "IntervalInSeconds": 60
                    },
                    "CompressionFormat": "UNCOMPRESSED",
                    "EncryptionConfiguration": {
                        "NoEncryptionConfig": "NoEncryption"
                    },
                    "CloudWatchLoggingOptions": {
                        "Enabled": false
                    },
                    "ProcessingConfiguration": {
                        "Enabled": false,
                        "Processors": []
                    },
                    "S3BackupMode": "Disabled",
                    "DataFormatConversionConfiguration": {
                        "Enabled": false
                    }
                }
            }
        ],
        "HasMoreDestinations": false
    }
}
```

#### 4. IAM ロール，関連付けるポリシーの作成：CloudWatch Logs to Firehose

- IAM ロールを作成し，CloudWatch Logs に Kinesis Data Firehose 送信ストリームにデータを置く権限を付与する．まず，テキストエディタを使用してファイル `TrustPolicyForCWL.json` で信頼ポリシーを作成する．

```json
{
  "Statement": {
    "Effect": "Allow",
    "Principal": { "Service": "logs.ap-northeast-1.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }
}
```

- `create-role` コマンドを使用し，信頼ポリシーファイルを指定して IAM ロールを作成する
  - 後のステップで必要になるため，返された Role.Arn 値を書き留める

```sh
aws iam create-role \
    --role-name cloudwatch-logs-to-firehose \
    --assume-role-policy-document file://./TrustPolicyForCWL.json

# 出力
{
    "Role": {
        "Path": "/",
        "RoleName": "cloudwatch-logs-to-firehose",
        "RoleId": "AROAXDX72D5ZZTTK6FBNJ",
        "Arn": "arn:aws:iam::489089015667:role/cloudwatch-logs-to-firehose",
        "CreateDate": "2020-11-06T04:26:31+00:00",
        "AssumeRolePolicyDocument": {
            "Statement": {
                "Effect": "Allow",
                "Principal": {
                    "Service": "logs.ap-northeast-1.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        }
    }
}
```

- 権限ポリシーを作成し，CloudWatch Logs がアカウントで実行できるアクションを定義する
  - まず，テキストエディタを使用して権限ポリシーファイル（例: `PermissionsForCWL.json`）を作成する
  - 下記 JSON ファイルの `Resource` を Firehose の ARN に対応するように書き直す

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["firehose:*"],
      "Resource": ["arn:aws:firehose:region:123456789012:*"]
    }
  ]
}
```

- `put-role-policy` コマンドを使用して，権限ポリシーをロールに関連付ける

```sh
aws iam put-role-policy --role-name cloudwatch-logs-to-firehose --policy-name Permissions-Policy-For-CWL --policy-document file://./PermissionsForCWL.json
```

#### 5. サブスクリプションフィルタの設定

Amazon Kinesis Data Firehose ストリームが Active 状態になり，IAM ロールを作成したら，CloudWatch Logs サブスクリプションフィルタを作成できる．サブスクリプションフィルタにより，選択されたロググループから Amazon Kinesis Data Firehose 送信ストリームへのリアルタイムログデータの流れがすぐに開始される．

- `describe-subscription-filters` コマンド
  - 現在のサブスクリプションフィルタの確認する
  - ここでは，環境変数 `${CWL_LOG_GROUP_NAME}`に設定したロググループのサブスクリプションフィルタを確認している

```sh
$ aws logs describe-subscription-filters --log-group-name "${CWL_LOG_GROUP_NAME}"
# まだ何もない
# {
    # "subscriptionFilters": []
# }
```

- `put-subscription-filter` コマンド
  - サブスクリプションフィルタを作成する
  - ここでは，サブスクリプションフィルタのフィルターパターンは `""` にしてすべてのログイベントを出力している

```sh
aws logs put-subscription-filter \
    --log-group-name "${CWL_LOG_GROUP_NAME}" \
    --filter-name "${SUBSCRIPTION_FILTER_NAME}" \
    --filter-pattern "" \
    --destination-arn "${KINESIS_FIREHOSE_ARN}" \
    --role-arn "${CWL_ROLE_ARN}"
```

- エラー出力に注意
  - 下記のエラーでは Firehose の配信ストリームが active かどうか確認しろとあるが，active でもエラーが出る場合，IAM ロールの設定がおかしい場合が多い
  - 結論エラーメッセージが悪い

```sh
An error occurred (InvalidParameterException) when calling the PutSubscriptionFilter operation: Could not deliver test message to specified Firehose stream. Check if the given Firehose stream is in ACTIVE state.
```

#### 6. サブスクリプションフィルタの動作確認

サブスクリプションフィルタを設定したら，CloudWatch Logs によりフィルタパターンに一致するすべての受信ログイベントが Amazon Kinesis Data Firehose 送信ストリームに転送される．データは，Amazon Kinesis Data Firehose 配信ストリームに設定された時間の間隔（デフォルトでは 300 sec），データサイズ（デフォルトでは 5 MB）に基づいて，Amazon S3 に表示される．十分な時間が経過すると，Amazon S3 バケットをチェックしてデータを確認できる．

```sh
aws s3api list-objects --bucket "test-cloudwatch-logs-to-s3"
{
    "Contents": [
        {
            "Key": "2020/11/06/04/test-cloudwatch-logs-to-s3-2-2020-11-06-04-57-58-303e3203-e31b-4c6a-bbcd-e2e801cce9cb",
            "LastModified": "2020-11-06T04:59:02+00:00",
            "ETag": "\"569537ed3dd83b87463fb17499d032db\"",
            "Size": 198,
            "StorageClass": "STANDARD",
            "Owner": {
                "DisplayName": "iko-13135",
                "ID": "d00d0e84b3e209e9fb7df9b56f1afd79a3b0ad32aced507105579f94f3e4dfb6"
            }
        },
        {
            "Key": "2020/11/06/05/test-cloudwatch-logs-to-s3-2-2020-11-06-05-03-49-20e68c01-23fb-4451-9d19-03cd3e48ccd4",
            "LastModified": "2020-11-06T05:04:52+00:00",
            "ETag": "\"f52b83ee34a3e873577c3eb99c208c30\"",
            "Size": 1963,
            "StorageClass": "STANDARD",
            "Owner": {
                "DisplayName": "iko-13135",
                "ID": "d00d0e84b3e209e9fb7df9b56f1afd79a3b0ad32aced507105579f94f3e4dfb6"
            }
        }
    ]
}
```

上記の各オブジェクトの Key 名を利用して gzip 形式でダウンロードする．Amazon S3 オブジェクトのデータは gzip 形式で圧縮される．

```sh
aws s3api get-object --bucket 'test-cloudwatch-logs-to-s3' --key '2020/11/06/05/test-cloudwatch-logs-to-s3-2-2020-11-06-05-03-49-20e68c01-23fb-4451-9d19-03cd3e48ccd4' testfile.gz
```

gzip 形式の raw データは，コマンドラインから次の UNIX コマンドを使用して調べることができる．CloudWatch Logs のログは JSON 形式のため，解凍の結果を JSON ファイルに吐くと中身がエディタなどで見やすい状態で見れる．

```sh
zcat testfile.gz
# Mac の場合 zcat を使うと以下のエラーで怒られる
zcat: can't stat: xxx.gz (xxx.gz.Z): No such file or directory'

# 代わりに gzcat コマンドを使用すれば OK
gzcat testfile.gz > test.json
```

### 補足：ログの整形

ログの整形を行う場合は以下の 2 通りがある．

- Firehose の中で "Transformation" という Lambda を発火させてログを（メタデータを除去したり，集計用に整形する）変換するための仕組みを用いる
- S3 に吐かれたログをトリガーにログを変換する Lambda を用いる

---

## 整理

- CloudWatch Logs のログの Firehose 経由での出力先となる S3 バケットの作成
- IAM ロールの作成：`firehose-to-s3`
  - Firehose が S3 バケットにデータを置く権限を付与するためのロール
  - 権限ポリシーの作成とロールへの関連付け `PermissionsForFirehose.json`
- Kinesis Data Firehose 配信ストリームの作成
  - 下記 2 つを使う
    - S3 バケットの ARN
    - IAM ロール `firehose-to-s3` の ARN
- IAM ロールの作成：`firehose-to-s3`
  - CloudWatch Logs が Firehose の配信ストリームにデータを置く権限を付与するためのロール
  - 権限ポリシーの作成とロールへの関連付け `PermissionsForCWL.json`
- 純粋なログデータが欲しいタイムスタンプとメッセージ
- S3 をトリガーで avro へ変換
- とりあえずぽちぽち
  - SAM
