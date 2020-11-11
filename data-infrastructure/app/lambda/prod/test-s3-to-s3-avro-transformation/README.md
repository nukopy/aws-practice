# test-s3-to-s3-avro-transformation

S3 へアップロードされた JSON line 形式のログファイル（以下）を Avro 形式のファイルへ変換する．
変換のトリガーは，そのログファイルが S3 へアップロードされたとき．

## Deploy

- Lambda 関数のデプロイパッケージの作成

```sh
$ sh ./create-deploy-package.sh
```

- Lambda 関数のデプロイ

```sh
$ sh ./deploy.sh
```
