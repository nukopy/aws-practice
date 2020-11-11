# test-s3-to-s3-avro-transformation

S3 へアップロードされた JSON line 形式のログファイル（以下）を Avro 形式のファイルへ変換する．
変換のトリガーは，そのログファイルが S3 へアップロードされたとき．

## 変換のステップ

以下，システムアーキテクチャ

![](../test-enjou-system-architecture.png)

- [x] トリガーされる Lambda を作成する（`print(event)` でログ出力を確認）
- [x] 2 つの S3 バケットを作成：ログファイル用，Avro 返還後のログファイル用
- [x] まずは，イベント駆動ではなく，lambda 関数の `event` 引数にアップロードのイベントを渡して Lambda のコンソールからテストを実行
  - [x] S3 にログファイルのサンプルをアップロード
  - [x] ローカルに `event.json` を保存
  - [x] コマンドラインから Lambda 関数を invoke
- [ ] S3 にファイルをアップロードしたのをトリガーに Lambda を発火し avro へ変換（3 h）
  - [ ] S3 にファイルアップロードしたのをトリガーに Lambda を発火させる
  - [x] Lambda でファイル操作を行う 1: ファイル名をログへ出力
  - [x] Lambda でファイル操作を行う 2: ファイル名をログへ出力し，avro 形式へ変換したものを S3 に保存

## Deploy

- Lambda 関数のデプロイパッケージの作成

```sh
$ sh ./create-deploy-package.sh
```

- Lambda 関数のデプロイ

```sh
$ sh ./deploy.sh
```
