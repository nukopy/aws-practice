# データ基盤の練習

練習の流れ

1. DynamoDB のレコードの更新（変更・追加など）を検知して Lambda を発火する
2. Lambda から DynamoDB の変更検知分を JSON 形式で Kinesis firehose へ流す
3. firehose 内で Lambda 発火して Avro 形式へ変換する
4. Avro 形式を S3 へ流す

## TODO

Hello world のために必要なこと

- [ ] DynamoDB でテーブルを作成し，データを準備する
  - テーブル設計は適当で OK
  - [ ] DynamoDB へ 100 レコード分のデータを入れる
- [ ] Lambda の作成
  - [ ] DynamoDB のテーブルの変更をトリガーにする
  - [ ] DynamoDB のデータを読み取り，JSON に変換する
  - [ ] JSON を Amazon Kinesis Firehose へ流す
- [ ] Firehose での処理
  - [ ] Lambda から JSON が送られてくる
  - [ ] データが送られてきたのをトリガーに Lambda を発火させ，JSON を Avro 形式へ変換する
  - [ ] Avro 形式のファイルを S3 に流す
    - [ ] 1 day，1 hour 単位など，データを流す周期を変更できるようにする

---

## 炎上のデータ基盤，ログ基盤

### やったこと

- DynamoDB 〜 S3 に Avro を吐き出す流れの実装

### これからやること

- ひとまずの TODO
  - CloudWatch Logs の検証
    - サブスクリプションフィルタの登録・動作確認
      - Lambda 関数の作成に伴って作られるロググループを用いると print デバッグできて楽
  - Avro in S3 の検証
    - S3 に保存したときに Avro 変換をできるか
  - TODO の分解（タスクの分解）

- 最終目標
  - DynamoDB 更新 -> Firehose -> JSON のまま S3 -> S3 の保存をトリガーに Avro 変換を走らせる
  - CloudWatch Logs 更新 -> Firehose -> JSON のまま S3 -> S3 の保存をトリガーに Avro 変換を走らせる
    - Firehose で Lambda を発火してメタデータとかのフィルタリングを行う

### TODO の分解

- 一旦 DynamoDB から新しく作り直す？
  - 既存のものは残しておく
- CloudWatch Logs の検証
  - ストリームの作成
  - ロググループの作成
  - サブスクリプションフィルタの作成