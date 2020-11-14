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

スクリプト内で行っているのは以下の 2 つの処理：

- Lambda のデプロイパッケージのアップロード
  - 「準備」のセクションで作成した S3 バケットへ Lambda の deploy package をアップロードし，そのリソース ID を含んだテンプレートファイルを生成する
- ETL タスクのスタックの作成

#### スタック作成に失敗したとき

スタックの作成に失敗した場合，コンソールでスタック作成時のログを確認し，スタックの消去を行う必要がある．
ブラウザの方が見やすいが，CLI で確認したい場合，以下のコマンドを実行する．

```sh
# スタック作成時のログを確認
# JSON 形式のログファイルで `CREATE_FAILED` を検索するスタック作成時のエラー原因が分かる
sh utils/log.sh [STACK NAME]

# スタックの消去（これをしないと同じ名前のスタックを新しく作成できない）
sh utils/delete-stack [STACK NAME]  # スタックの消去
```

### テスト

- テストの手順
  - ETL タスクのエントリーポイントである Lambda 関数 `lambda-entry-point` のコンソールへ移動し，「テスト」を何回か実行する
    - この部分はログのソースとなるため，実際のプロダクトでは他のサービスに置き換わる可能性がある．ここでは，デバッグを楽にするために，Lambda 関数による CloudWatch Logs へのログ出力により，後続の ETL タスクが発火するようになっている
    - **注意：ETL タスクの結果は S3 バケットへ吐かれるが，Firehose のバッファリングの設定により，ログが S3 へ吐かれるまで数分かかる可能性がある**
  - 以下 2 つの S3 バケットの中身を確認し，オブジェクトをローカルに保存する．`output` ディレクトリに，それぞれ `log`，`log.avro` というファイル名でダウンロードする
    - JSON-line 形式のログが吐かれる S3 バケット：`test-enjou-log-etl-cfn-s3-bucket-logging`
    - Avro 形式のログが吐かれる S3 バケット：`test-enjou-log-etl-cfn-s3-bucket-logging-avro`
  - 以下のスクリプトで簡易的なテストを実行
    - テスト項目
      - Avro 形式のファイルが読み込めるか
      - ログの圧縮処理の前後で内容が一致するか

```sh
python test_output.py
```
