# AWS Lambda について

## Serverless Framework

- install

```sh
$ npm -g install serverless

# restart shell
$ serverless --version
Framework Core: 2.10.0
Plugin: 4.1.1
SDK: 2.3.2
Components: 3.3.0
```

## Serverless Framework における "service" という概念

"service" はプロジェクトのようなもの．

- AWS Lambda Functions
- Lambda に定義した関数をトリガーとするイベント
- 必要な AWS インフラストラクチャリソース

を定義し，全て `serverless.yml` というファイルにまとめる．

## Creation of "service"

サービスを作成するには，`create` コマンドを使用する．また，サービスを記述するランタイム（node.js，python など）を指定する必要がある．また，パスを渡すことでディレクトリを作成し，サービスに自動で名前を付けることもできる．

- create コマンド
  - ドキュメント：[AWS - Create](https://www.serverless.com/framework/docs/providers/aws/cli-reference/create/)

```sh
$ serverless create --template aws-python3 --path my_service
```

- Here are the available templates for AWS Lambda:
  - aws-clojurescript-gradle
  - aws-clojure-gradle
  - aws-nodejs
  - aws-nodejs-typescript
  - aws-alexa-typescript
  - aws-nodejs-ecma-script
  - aws-python
  - aws-python3
  - aws-ruby
  - aws-provided
  - aws-kotlin-jvm-maven
  - aws-kotlin-nodejs-gradle
  - aws-groovy-gradle
  - aws-java-gradle
  - aws-java-maven
  - aws-scala-sbt
  - aws-csharp
  - aws-fsharp
  - aws-go
  - aws-go-dep
  - aws-go-mod

### `create` コマンドで作成されるファイル

- `create` コマンドで作成されるファイル
  - `serverless.yml`
  - `handler.py`（ランタイムによる．TypeScript の場合 `handler.ts`．）

### serverless.yml

各サービスの設定は，`serverless.yml` ファイルで管理される．このファイルの主な役割は以下の通り．

- Serverless サービスの宣言
- サービスに1つ以上の機能を定義する
- サービスがデプロイされるプロバイダ（プロバイダは AWS や GCP など．ランタイムもここに記述される．)
- 使用するカスタムプラグインの定義
- 各関数の実行のトリガーとなるイベントを定義します（HTTPリクエストなど）。
- このサービスの機能が必要とするリソースのセット（例：1 DynamoDBテーブル）を定義します。
- イベントセクションにリストされているイベントが、デプロイ時にイベントに必要なリソースを自動的に作成できるようにします。
- サーバーレス変数を使用した柔軟な設定が可能
- `handler.py`ファイルを指す関数定義の中に、サービスの名前、プロバイダの設定、最初の関数があります。それ以上のサービスの設定はこのファイルで行います。