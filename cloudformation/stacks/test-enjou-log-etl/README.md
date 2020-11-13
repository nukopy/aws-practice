# test-enjou-log-etl

AWS CloudFormation を用いて，ログを処理する ETL タスクのためのリソースのプロビジョニングを行う．

## インフラ構成

### ETL タスクの流れ

```txt
AWS Lambda --> CloudWatch Logs --(サブスクリプションフィルタ)--> Firehose -> S3
```

### システムアーキテクチャ

![img](./docs/img/test-enjou-system-architecture.png)

### AWS リソース

resouce prefix: `test-enjou-log-etl-cfn`

TODO: 他のリソースを正確に書く

- **AWS IAM**
  - IAM Role
  - IAM Managed Policy
- **AWS Lambda**
  - [x] `lambda-entry-point`
  - [x] `lambda-firehose-logging-transformation`
  - [x] `lambda-s3-avro-transformation`
- **Amazon CloudWatch Logs**
  - Log Group
  - Subscription Filter
- **Amaozn S3**
  - [x] `s3-bucket-logging`
  - [x] `s3-bucket-logging-avro`
- **Amazon Kinesis Data Firehose**
  - Delivery Stream

### その他 AWS リソース

- **Amazon S3**
  - [x] `s3-bucket-lambda-deploy-packages`
    - ETL タスク用のスタック作成前に，この S3 バケットを CFn で作成する必要がある

## デプロイ

### 準備

TODO: 一時的なバケットを作成して終わったらそれを消去するとかできたらいいね．

- Lambda の Deploy Package の zip 用の S3 バケットを作成しておく
  - 引数 `deploy` を渡さない場合，変更セットの作成で止まる

```sh
git clone [URL]
cd aws-practice/cloudformation/stacks/test-enjou-log-etl
sh deploy-s3-bucket-for-lambda-deploy-packages.sh deploy
```

### スタックの作成

- スタックの作成

```sh
# 引数 `deploy` を渡さない場合，変更セットの作成で止まる
sh deploy.sh deploy
```

- スタックの作成に失敗した場合
  - スタック作成時のログを取得
  - スタックの消去

```sh
sh utils/log.sh [STACK NAME]  # エラーログの出力
sh utils/delete-stack [STACK NAME]  # スタックの消去
```

スクリプト内で行っているのは以下の 2 つの処理：

- Lambda のデプロイパッケージのアップロード
  - 「準備」のセクションで作成した S3 バケットへ Lambda の deploy package をアップロードし，そのリソース ID を含んだテンプレートファイルを生成する
- ETL タスクのスタックの作成

### テスト

ETL タスクのエントリーポイントである Lambda 関数 `lambda-entry-point` のコンソールへ移動し，「テスト」を何回か実行する．
これにより，CloudWatch Logs へログが吐かれ，それをトリガーとしてログ処理の ETL タスクが動く．
ETL タスクの結果は S3 バケットへ吐かれるが，Firehose のバッファリングの設定により，ログが S3 へ吐かれるまで数分かかる可能性がある．

- テスト結果の確認
  - 以下 2 つの S3 バケットの中身を確認し，オブジェクトをローカルのディレクトリ `output/log`，`output/log-avro` にそれぞれダウンロードする．
    - JSON-line 形式のログが吐かれる S3 バケット
    - Avro 形式のログが吐かれる S3 バケット
  - 以下のスクリプトを実行
    - Avro 形式のログが読み込めるかのテスト

```sh
python test_output.py
# Avro のファイルがちゃんと読み込めて出力されればパイプラインの構築ができている
```

## メモ

- CloudFormation 上の Stack の消去

```sh
sh utils/delete-stack [STACK NAME]
```

- スタックのエラーログの見方
  - JSON 形式のログファイルから `CREATE_FAILED` を探すと原因が分かる

```sh
sh utils/log.sh [STACK NAME]
```
