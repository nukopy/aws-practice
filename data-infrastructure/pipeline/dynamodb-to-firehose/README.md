# dynamodb-to-firehose

- Kinesis データストリームの検証
  - Amazon Kinesis Data Streams for DynamoDB を使用し，テーブルの項目レベルの変更を Kinesis データストリームとしてキャプチャする
  - 公式 doc
    - [Change Data Capture for Kinesis Data Streams](https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/kds.html)
    - [DynamoDB ストリーム を使用したテーブルアクティビティのキャプチャ](https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/Streams.html)

## deploy

```sh
# deploy
sh deploy.sh deploy

# delete stack
sh delete-stack.sh
```

## DynamoDB のテーブルの変更のキャプチャ

DynamoDB のテーブルの項目が変更されたとき，それをキャプチャすることができる．
キャプチャする方法としては，以下の 2 つがある．

- DynamoDB ストリーム
- Amazon Kinesis Data Streams for DynamoDB

## DynamoDB ストリーム

公式 doc：[DynamoDB ストリーム を使用したテーブルアクティビティのキャプチャ](https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/Streams.html)

- DynamoDB ストリーム
  - DynamoDB テーブルの項目の変更内容のログを溜めておくバッファのようなもの
  - DynamoDB ストリームは，ストリームレコードをほぼリアルタイムで書き込むため，これらのストリームを使用し，テーブルの項目の更新情報をキャプチャし，その更新情報に基づいた別の AWS アプリケーションの処理を設定することができる
- DynamoDB ストリームレコード
  - DynamoDB テーブルの項目の変更内容のログ
  - リアルタイムで DynamoDB ストリームに流される
  - 各ストリームレコードは，ストリームに 1 回だけ出現する
  - DynamoDB テーブルで変更された各項目について，ストリームレコードは項目に対する実際の変更と同じ順序で出現する

DynamoDB ストリームは，DynamoDB テーブル内の項目に加えられた変更に関する情報の順序付けされた情報である．
テーブルでストリームを有効にすると，DynamoDB はテーブル内のデータ項目に加えられた各変更に関する情報をキャプチャする．

アプリケーションがテーブル内の項目を作成，更新，または削除するたびに，DynamoDB ストリーム は変更された項目のプライマリキー属性を付けてストリームレコードを書き込む．
ストリームレコードには，DynamoDB テーブル内の単一の項目に加えられたデータ変更についての情報が含まれている．
ストリームレコードが追加情報（変更された項目の前後のイメージ）をキャプチャするようにストリームを設定できる．

### 項目

- DynamoDB ストリーム and TTL
- DynamoDB ストリーム Kinesis Adapter を使用したストリームレコードの処理
- DynamoDB ストリーム の低レベル API: Java の例
- クロスリージョンレプリケーション
- DynamoDB ストリーム と AWS Lambda のトリガー

## Amazon Kinesis Data Streams for DynamoDB

- テーブルの項目レベルの変更を Kinesis データストリームとしてキャプチャする
