# test-enjou

AWS Lambda --> CloudWatch Logs --(サブスクリプションフィルタ)--> Firehose -> S3

- System Architecture

![img](./docs/img/test-enjou-system-architecture.png)

## AWS リソース

パイプラインで使用しているリソース一覧

TODO: いろいろ整ってからで良い

- **AWS Lambda**
  - `test-enjou-cloudwatch-logs-to-s3`
    - パイプラインのデバッグを楽にするために作成した
      - Lambda のコンソールのテストからすぐにログを流せる
    - サブスクリプションフィルタに登録するロググループを作る
  - `test-enjou-cloud-watch-logs-to-s3-firehose-transformation`
    - Firehose 上でログを整形するための関数
      - メタデータの除去
      - JSON 形式として吐かれたログのみを取得するためのフィルタリング
    - JSON-line 形式のログを吐く
  - `test-enjou-s3-to-s3-avro-transformation`
    - S3 に JSON-line 形式のログが吐かれたのをトリガーに，それを Avro 形式に変換するための関数
- **CloudWatch Logs**
  - `/aws/lambda/test-enjou-cloudwatch-logs-to-s3`
    - Lambda 関数 `test-enjou-cloudwatch-logs-to-s3` の作成により自動で作られるロググループ．この関数のログが吐かれる．
    - このロググループに対してサブスクリプションフィルタを登録すると，このロググループにログが吐かれる度に Firehose にログデータを流す
    - **このリソースに関係のある他の AWS リソース**
      - Firehose：`test-enjou-cloudwatch-logs-to-s3`
        - この配信ストリームにログを流す
- **Amazon Kinesis Data Firehose**
  - `test-enjou-cloudwatch-logs-to-s3`
    - 配信ストリーム．CloudWatch Logs からのログを S3 に "高速に" 横流しにする．
    - **このリソースに関係のある他の AWS リソース**
      - Lambda：`test-enjou-cloud-watch-logs-to-s3-firehose-transformation`
        - ログを流す際，この Lambda 関数を実行し，ログを整形する．整形後のログ（JSON-line 形式）が S3 バケット `test-enjou-cloudwatch-logs-to-s3` に吐かれる．
      - S3：`test-enjou-cloudwatch-logs-to-s3`
        - 配信ストリームのターゲットとなる S3 バケット．整形後のログ（JSON-line 形式）がこのバケットに吐かれる．
- **Amazon S3**
  - バケット 2 つ
    - `test-enjou-cloudwatch-logs-to-s3`
      - JSON-line 形式のログファイル用のバケット
      - ファイルアップロードにより，Lambda 関数 `test-enjou-s3-to-s3-avro-transformation` がトリガーされる
    - `test-enjou-cloudwatch-logs-to-s3-avro`
      - Avro 形式に変換後のログファイル用のバケット
      - Lambda 関数 `test-enjou-s3-to-s3-avro-transformation` により，このバケットに Avro 形式のファイルが吐かれる
- IAM
  - TODO: 各サービスがどのサービスへのアクセス権限があるかというのを定義するための色んなロールが必要になる