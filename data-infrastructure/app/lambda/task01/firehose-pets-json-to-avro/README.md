# デプロイの手順

- コンテナ側で `lambda-deploy-package.sh` を実行
  - linux 環境での Python ライブラリのビルド

```sh
# in container
sh lambda-deploy-package.sh
```

- ホスト側で `deploy.sh` を実行
  - AWS に関する認証情報をコンテナに渡してない，かつ aws コマンドがない
  - 恐らく Lambda 用の Docker コンテナとか用意されてるからいずれはそっちにしたい

```sh
sh deploy.sh
```
