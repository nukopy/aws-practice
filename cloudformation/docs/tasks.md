# タスクの整理

## 2020/11/12

- [ ] ここまでの流れを全て SAM（CloudFormation）でデプロイできるようにする
  - [x] CloudFormation，SAM のキャッチアップ
    - [x] そもそも CloudFormation，SAM が何なのかを知る
    - [x] まずは Lambda の一番単純なやつからデプロイ．
      - IAM のロールとかポリシー周りでハマりそう
      - ちょっとずつデプロイする範囲を広げていく．いきなりでかくデプロイしない．
  - CFn で各リソースのデプロイ
    - [x] IAM ロールのデプロイ
    - [x] Lambda with IAM ロールのデプロイ
    - [x] S3 のデプロイ
    - [x] Lambda with CloudWatchLogs のデプロイ
    - [ ] S3 with Lambda のデプロイ（Lambda でトリガーされるやつ）
    - [x] Kinesis 配信ストリームのデプロイ
    - [x] Kinesis 配信ストリームのデプロイ with サブスクリプションフィルターのデプロイ
    - [ ] test-enjou-etl 全体をデプロイ

申し送り

- 明日は Lambda を作成したときに CloudWatch Logs にロググループが作成できるようにするとこから

## 2020/11/13 日報

### やったこと

- ログ処理の ETL の一連のスタックの構築
- サブスクリプションフィルタの設定も終わり，デバッグ用の Lambda からログを流すと，JSON-line 形式のログが S3 バケットへ吐かれるところまで出来た

### これから

- 3 ~ 4 h 程度
  - S3 へ JSON-line 形式のログをアップロードしたときに，Avro 変換用の Lambda をトリガーさせる設定を CFn に記述する
  - S3 の通知周りの仕組みをもう少し理解する必要がありそう
  - 参考リンク：公式 doc https://aws.amazon.com/jp/premiumsupport/knowledge-center/cloudformation-s3-notification-lambda/
