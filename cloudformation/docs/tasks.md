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
    - [ ] Lambda with CloudWatchLogs のデプロイ
    - [ ] S3 with Lambda のデプロイ（Lambda でトリガーされるやつ）
    - [ ] Kinesis 配信ストリームのデプロイ
    - [ ] Kinesis 配信ストリームのデプロイ with サブスクリプションフィルターのデプロイ
    - [ ] test-enjou-etl 全体をデプロイ

申し送り

- 明日は Lambda を作成したときに CloudWatch Logs にロググループが作成できるようにするとこから
