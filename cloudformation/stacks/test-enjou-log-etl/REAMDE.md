# test-enjou

AWS CloudFormation でログを処理する ETL タスクのリソースの定義

## システムアーキテクチャ

- 目的のリソース群

```txt
AWS Lambda --> CloudWatch Logs --(サブスクリプションフィルタ)--> Firehose -> S3
```

- システムアーキテクチャ

![img](./docs/img/test-enjou-system-architecture.png)


## デプロイ

### 準備

- Lambda の Deploy Package の zip 用の S3 バケットを作成しておく
  - `deploy` を渡さないと変更セットの作成で止まる

```sh
sh create-bucket-for-lambda-deploy-packages.sh deploy
```

### スタックの作成

- Lambda のデプロイパッケージのアップロード
  - 「準備」のセクションで作成した S3 バケットへ Lambda の deploy package をアップロードし，そのリソース ID を含んだテンプレートファイルを生成する

```sh
sh upload-lambda-deploy-packages.sh
```

- ETL タスクのスタックの作成

```sh
sh deploy.sh deploy

# スタックの作成に失敗したら
sh utils/log.sh [STACK NAME]  # エラーログの出力
sh utils/delete-stack [STACK NAME]  # スタックの消去
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