# AWS Lambda を Amazon S3 に使用する

何はともあれ，まずはドキュメントをちゃんと読む．

- [AWS Lambda を Amazon S3 に使用する](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/with-s3.html)
- [チュートリアル：AWS Lambda を Amazon S3 に使用する](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/with-s3-example.html)

## 概要

Lambda を使用して Amazon Simple Storage Service からのイベント通知を処理できる．
**Amazon S3 は，オブジェクトの作成時や削除時にイベントを Lambda 関数に送信できる**．
バケットの通知設定を構成し，関数のリソースベースのアクセス許可ポリシーで関数を呼び出すためのアクセス許可を Amazon S3 に付与する．

```txt
- 警告

Lambda 関数で使用するバケットが，その関数をトリガーするのと同じバケットである場合，関数はループで実行される可能性がある．
例えば，オブジェクトがアップロードされるたびにバケットで関数をトリガーし，その関数によってオブジェクトがバケットにアップロードされると，
その関数によって間接的にその関数自体がトリガーされる．これを回避するには，2 つのバケットを使用するか，受信オブジェクトで使用されるプレフィックスにのみ適用されるようにトリガーを設定する．

- 再帰呼び出し
関数が S3 バケットにオブジェクトを書き込む場合は，入出力に異なる S3 バケットを使用すること．
同じバケットに書き込むと，再帰呼び出しを生み出すリスクが高くなり，その結果，Lambda の使用量が増加してコストが増大する可能性がある．
入力と出力の両方に同じ S3 バケットを使用することは推奨されておらず，この設定により，再帰呼び出しが生じ，
それに伴い Lambda の使用量増加，コスト増大の可能性があることを認識する必要がある．
```

Amazon S3 は，オブジェクトに関する詳細を含むイベントで非同期に関数を呼び出す．
次の例は，デプロイパッケージが Amazon S3 にアップロードされたときに Amazon S3 から送信されたイベントを示している．

- 例 Amazon S3 通知イベント
  - Lambda 関数の `event` に渡される JSON オブジェクト

```json
{
  "Records": [
    {
      "eventVersion": "2.1",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-2",
      "eventTime": "2019-09-03T19:37:27.192Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "AWS:AIDAINPONIXQXHT3IKHL2"
      },
      "requestParameters": {
        "sourceIPAddress": "205.255.255.255"
      },
      "responseElements": {
        "x-amz-request-id": "D82B88E5F771F645",
        "x-amz-id-2": "vlR7PnpV2Ce81l0PRw6jlUpck7Jo5ZsQjryTjKlc5aLWGVHPZLj5NeC6qMa0emYBDXOo6QBU0Wo="
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "828aa6fc-f7b5-4305-8584-487c791949c1",
        "bucket": {
          "name": "lambda-artifacts-deafc19498e3f2df",
          "ownerIdentity": {
            "principalId": "A3I5XTEXAMAI3E"
          },
          "arn": "arn:aws:s3:::lambda-artifacts-deafc19498e3f2df"
        },
        "object": {
          "key": "b21b84d653bb07b05b1e6b33684dc11b",
          "size": 1305107,
          "eTag": "b21b84d653bb07b05b1e6b33684dc11b",
          "sequencer": "0C0F6F405D6ED209E1"
        }
      }
    }
  ]
}
```

関数を呼び出すには，関数のリソースベースのポリシー（[AWS Lambda のリソースベースのポリシーを使用する](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/access-control-resource-based.html)を参照）によるアクセス許可が Amazon S3 に必要である．
Lambda コンソールで Amazon S3 トリガーを設定すると，バケット名とアカウント ID が一致した場合に Amazon S3 で関数を呼び出せるように，コンソールでリソースベースのポリシーが変更される．
Amazon S3 の通知を設定する場合は，Lambda API を使用してこのポリシーを更新する．
また，Lambda API を使用して，別のアカウントにアクセス許可を付与したり，指定されたエイリアスへのアクセス許可を制限したりできる．

関数で AWS SDK を使用して Amazon S3 リソースを管理する場合は，その実行ロールに Amazon S3 のアクセス許可も必要である．

---

## チュートリアル：AWS Lambda を Amazon S3 に使用する

- 目的
  - バケットにアップロードされる各ログファイルを Avro 形式に変換し，返還後のファイルを別のバケットへする．

オブジェクトの作成時に Amazon S3 が呼び出すことができる Lambda 関数（CreateThumbnail）を作成できる．
その後，Lambda 関数はソースバケットから画像オブジェクトを読み取り，ターゲットバケットにサムネイル画像を作成できる．

このチュートリアルを完了すると，アカウントで以下の Amazon S3，Lambda，および IAM リソースが作成される．

### 使用するリソース

- Lambda のリソース
  - Amazon S3 に Lambda 関数を呼び出すアクセス許可を付与する Lambda 関数に関連づけられたアクセスポリシーである
- IAM のリソース
  - このロールに関連付けられたアクセス権限ポリシーを使用して Lambda 関数に必要なアクセス許可を付与する実行ロール
- Amazon S3 のリソース
  - Lambda 関数を呼び出す通知設定を持つソースバケット．ログファイルがアップロードされる．
  - 関数が Avro 変換されたログファイルを保存するターゲットバケット

### ステップ

- [x] トリガーされる Lambda を作成する（`print(event)` でログ出力を確認）
- [x] 2 つの S3 バケットを作成：ログファイル用，Avro 返還後のログファイル用
- まずは，イベント駆動ではなく，lambda 関数の `event` 引数にアップロードのイベントを渡して Lambda のコンソールからテストを実行
  - [x] S3 にログファイルのサンプルをアップロード
  - [x] Lambda のコンソールでテストを実行
- [x] s3 にファイルをアップロード
- [ ] S3 にファイルをアップロードしたのをトリガーに Lambda を発火し avro へ変換（3 h）
  - [ ] S3 にファイルアップロードしたのをトリガーに Lambda を発火させる
  - [x] Lambda でファイル操作を行う 1: ファイル名をログへ出力
  - [x] Lambda でファイル操作を行う 2: ファイル名をログへ出力し，avro 形式へ変換したものを S3 に保存
