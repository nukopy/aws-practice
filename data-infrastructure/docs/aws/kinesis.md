# Amazon Kinesis

## ストリームデータ，ストリーミングデータとは

- ストリームデータ
  - 株取引情報や交通情報などのように，継続的に発生する，タイムスタンプ（生成または更新された時刻情報）を含むデータのこと．
  - データベースでのデータ処理が，入力されたデータを蓄積し，任意のタイミングで命令（クエリ）を発行する処理であるのに対し，ストリームデータ処理では，あらかじめクエリを登録しておくことで，データが入力されたタイミングでクエリが実行される．入力されたデータは，ストレージなどに貯めずに，メモリ上で順次処理していく．次々と到来するデータに対して，処理を継続的に行うことで，データ発生時からのタイムラグを抑え，リアルタイムな処理を実現している．
  - ストリームデータ処理の研究は，2000 年代初頭から始まった．国内では，ビジネスや日常生活で扱うデータ量が増えるにつれて，注目を集めるようになり，2000 年代後半にストリームデータ処理機能を搭載した製品が発売されている．今後は IoT の発展により，センサーデータの処理の需要が高まることが予想され，さらなる活用が期待される．

## Amazon Kinesis とは

Amazon Kinesis でストリーミングデータをリアルタイムで収集，処理，分析することが簡単になるため，インサイトを適時に取得して新しい情報に迅速に対応できる．

Amazon Kinesis は，アプリケーションの要件に最適なツールを柔軟に選択できるだけでなく，あらゆる規模のストリーミングデータをコスト効率良く処理するための主要機能を提供する．

Amazon Kinesis を使うと，機械学習，分析，その他のアプリケーションに用いる動画，音声，アプリケーションログ，ウェブサイトのクリックストリーム，IoT テレメトリーデータをリアルタイムで取り込める．Amazon Kinesis はデータを受信するとすぐに処理および分析を行うため，全てのデータを収集するのを待たずに処理を開始して直ちに応答することが可能である．

## Amazon Kinesis の用途

- サービスの連携部分（キューなどによる Pub/Sub システム）を決めるのは非常に重要でボトルネックになりやすい．それを解決するのが Kinesis．Kinesis 自体はデータフローを取り扱うサービス．RabbitMQ，Redis などとの違いは「**スケールするかしないか**」．RabbitMQ や Redis はボトルネックになりやすい．
- Kinesis Firehose は，中でもダムのような役割．

---

## Amazon Kinesis Data Firehose

- Prepare and load real-time data streams into data stores and analytics services
  - リアルタイムのデータストリームを準備し，データストアやアナリティクスサービスへロードする
  - パイプライン，ダムみたいなもの

Amazon Kinesis Data Firehose は，ストリーミングデータをデータレイク，データストア，アナリティクスサービスに確実にロードする最も簡単な方法である．Firehose はデータを取り込み，変換し，他のストレージサービスにデータをロードする，謂わばパイプラインの役割をする．

データのロードの対象としては，Amazon S3，Amazon Redshift，Amazon Elasticsearch Service，一般的な HTTP エンドポイント，Datadog，New Relic，MongoDB，Splunk などが挙げられる．これらのサービスプロバイダにストリーミングデータを配信することができる．

Firehose はフルマネージドなサービスであり，データのスループットに合わせて自動的にスケーリングし，ユーザによる継続的な管理は必要ない．
また，AWS Lambda 等と連携し，データのロード前にデータストリームをバッチ処理，圧縮，変換，暗号化することができるため，ストレージの使用量を最小限に抑え，セキュリティを向上させることができる．

AWS Management Console から簡単に Firehose 「**配信ストリーム**」を作成し，数回クリックするだけで設定し，何十万ものデータソースから指定した配信先へのストリーミングデータのインジェストを開始することができる．また，データストリームを設定することで，データが配信される前に，受信したデータを Apache Parquet や Apache ORC のようなオープンで標準ベースのフォーマットに自動的に変換することもできる．

Amazon Kinesis Data Firehose では，最低料金やセットアップ費用はない．
サービスを介して送信するデータ量，該当する場合はデータフォーマットの変換，Amazon VPC の配信とデータ転送のために支払うことになる．

### Firehose のメリット

- 使いやすい
  - Amazon Kinesis Data Firehose は，AWS Management Console で数回クリックするだけで，ストリーミングデータのキャプチャ，変換，ロードを簡単に行う方法を提供する．Firehose の配信ストリームを素早く作成し，配信先を選択して，何十万ものデータソースからリアルタイムのデータを同時に送信し始めることができる．指定した間隔でデータを送信先に継続的にロードするために必要なスケーリング，シャーディング，モニタリングなど，ストリームの管理は全てこのサービスが行う．

- AWS のサービスやサービスプロバイダとの統合
  - Amazon Kinesis Data Firehose は，Amazon S3，Amazon Redshift，Amazon Elasticsearch Service と統合されている．また，一般的な HTTP エンドポイントにデータを配信したり，Datadog，New Relic，MongoDB，Splunk などのサービスプロバイダに直接データを配信することもできる．AWS Management Console から、Kinesis Data Firehose を任意の配信先に向け、既存のアプリケーションやツールを使ってストリーミングデータの分析を行うことができます。

- サーバーレスのデータ変換
  Amazon Kinesis Data Firehose を使用すると、ストリーミングデータをデータストアにロードする前に準備することができます。Kinesis Data Firehose を使用すると、データソースからの生のストリーミングデータを、データストアが必要とする Apache Parquet や Apache ORC などの形式に簡単に変換することができ、独自のデータ処理パイプラインを構築する必要がありません。詳細はこちら "

- ニアリアルタイム
  Amazon Kinesis Data Firehose は、ほぼリアルタイムでデータをキャプチャしてロードします。データがサービスに送信されてから 60 秒以内に新しいデータを目的地にロードします。その結果、より早く新しいデータにアクセスし、ビジネスや運用上のイベントに素早く対応することができます。

- 継続的な管理は不要
  Amazon Kinesis Data Firehose は、ストリーミングデータの処理とロードに必要なコンピュート、メモリ、ネットワークリソースを自動的にプロビジョニング、管理、スケーリングする完全に管理されたサービスです。設定すると、Kinesis Data Firehose は、データストリームを配信先に継続的にロードします。

- 使用した分だけお支払い
  Amazon Kinesis Data Firehose を利用すると、お客様は、サービスを通じて送信するデータ量、および該当する場合はデータ形式の変換にかかる費用のみを支払うことになります。また、Amazon VPC の配信と、該当する場合はデータ転送のための費用もお支払いいただきます。最低料金や前払いのコミットメントはありません。

### Firehose の立ち上げ方

- "Transform source records with AWS Lambda" というレコードを変換するための Lambda 関数を作成する．
  - このとき，中身は `print(event)` くらいにして，CloudWatch Logs にログとして `event` の中身を吐き出すようにするとデバッグがしやすくなる．
  - Firehose に設定する前に，Lambda 単体で動くことをテストで確認しておく．恐らく `print(event)` くらいなら何も問題なくテストが動くはず．そして，Lambda のログが CloudWatch Logs に吐かれてることを確認する．これを確認しておかないと，デバッグできない．
  - Lambda をデバッグする時は `event.json` をテストにセットすると良い．
  - **必ず Lambda 単体で動くことを確認すること（Lambda のコンソール上の "テスト" にて，`event.json` を設定してそれを入力としてテストする）**
- Firehose のコンソールで配信ストリームを作成する
  - 先ほど作成した Lambda にデプロイした関数を設定する．これにより，配信ストリームにデータが送信されるたびに，S3 へ配信する前にその Lambda の関数を噛ませることができる．
    - Lambda 設定前：データソース -> Firehose -> S3
    - Lambda 設定後：データソース -> Firehose -> Firehose 内で Lambda を噛ませる -> S3
  - デバッグを快適に行うために，"Transform source records with AWS Lambda" の "**Buffer conditions**" を `60 seconds` に設定しておく．
    - これをしておかないと，Firehose へデータを送信してから，Firehose 内で Lambda を発火させるまでにデフォルトだと 300 秒かかってしまう．
- Firehose のコンソールからテストを実行する．
  - "Test with demo data" というセクションからテストデータを Firehose へロードすることができる．テストが実行されると，パイプラインが動き，最終成果物として S3 へ吐き出される．
  - デバッグは，Lambda のログ，S3 へ吐き出されているログを確認することにより行う．
  - Kinesis Firehose のログは，S3 か噛ませている Lambda でしか拾えない．

## Amazon Kinesis Data Firehose のデータ変換

- 公式 doc：[Amazon Kinesis Data Firehose のデータ変換](https://docs.aws.amazon.com/ja_jp/firehose/latest/dev/data-transformation.html)

Kinesis Data Firehose では，Lambda 関数を呼び出して，受信した送信元データを変換してから送信先に配信できる．Kinesis Data Firehose のデータ変換は，配信ストリームの作成時に有効にすることができる．

### 大前提

- transformation を動かす前に，現在の配信ストリームが Lambda への権限があるかをチェックする．そうしないとログが S3 に行かないと見れない．データ変換に指定した Lambda には呼び出されていないのでログが吐かれないし，Firehose のブラウザからのエラーも見れない．
- Firehose にデータを流し込んでも，バッファのせいで 5 min くらい経たないとログが吐かれないことがある．気長に待とう．

### データ変換フロー

Kinesis Data Firehose データ変換を有効にすると，Kinesis Data Firehose はデフォルトで最大 3 MB まで受信データをバッファする（バッファサイズを調整するには，`ProcessingConfiguration` API を `BufferSizeInMBs` と呼ばれる ProcessorParameter と共に使用する）．

- コメント
  - **Buffer size だと 6 MB までできるけど，データ変換利用すると少なくなるの？**

次に，Kinesis Data Firehose は，AWS Lambda 同期呼び出しモードを使用して，バッファされた各バッチで，指定された Lambda 関数を非同期的に呼び出す．

- コメント
  - **どの単位で Lambda の呼び出しが起こり，どの単位でデータ変換後のデータが送信されるのか？**

変換されたデータは，Lambda から Kinesis Data Firehose に送信される．
その後，変換されたデータは，**指定された送信先のバッファサイズとバッファ間隔のいずれかに到達したとき**，Kinesis Data Firehose より送信先に送信される．到達順序は関係ない．

- 重要
  - **Lambda 同期呼び出しモードには，リクエストとレスポンスの両方について，ペイロードサイズに 6 MB の制限がある**
  - **関数にリクエストを送信するためのバッファサイズが 6 MB 以下であることを確認すること．また，関数より返るレスポンスが 6 MB を超えないことを確認すること．**

### データ変換とステータスモデル

Lambda からの全ての変換されたレコードには，以下のパラメータが含まれる必要がある．含まれない場合，Kinesis Data Firehose はそれらのレコードを拒否し，データ変換の失敗として処理する．

- `recordId`
  - レコード ID は，呼び出し時に Kinesis Data Firehose から Lambda に渡される．変換されたレコードには，同じレコード ID が含まれる必要がある．元のレコードの ID と変換されたレコードの ID との不一致は，データ変換失敗として扱われる．
  - つまり，**Lambda の event として送られてきたレコードのレコード ID は変換の前後で変わってはいけない**

- `result`
  - レコードのデータ変換のステータス
  - 指定できる値は次のとおり：
    - `Ok`（レコードが正常に変換された）
    - `Dropped`（レコードが処理ロジックによって意図的に削除された）
    - `ProcessingFailed`（レコードを変換できなかった）
  - レコードのステータスが `Ok` または `Dropped` の場合，Kinesis Data Firehose はレコードが正常に処理されたとみなす．それ以外の場合，Kinesis Data Firehose はレコードが処理に失敗したとみなす．
- `data`
  - base64 エンコード後の変換されたデータペイロード
  - Python 内で base64 エンコードされた str 型に変換しないといけない
    - `"[base64 に変換された文字列]\n"`

## Lambda 設計図（Lambda blueprint）

データ変換用の Lambda 関数を作成するために使用できる設計図があります。これらの設計図の一部は AWS Lambda コンソールにあり、一部は AWS Serverless Application Repository にあります。

AWS Lambda コンソールで使用可能な設計図を表示するには

AWS マネジメントコンソール にサインインし、https://console.aws.amazon.com/lambda/ にある AWS Lambda コンソールを開きます。

[関数の作成]、[Use a blueprint (設計図の使用)] の順に選択します。

[設計図] フィールドで、キーワード firehose で検索して Kinesis Data Firehose Lambda 設計図を見つけます。

AWS Serverless Application Repository で使用可能な設計図を表示するには

AWS Serverless Application Repository に移動します。

Browse all applications を選択します。

[アプリケーション] フィールドで、キーワード firehose を検索します。

設計図を使用せずに Lambda 関数を作成することもできます。「AWS Lambda の開始方法」を参照してください。

### データ変換失敗の処理

ネットワークタイムアウトのために，または Lambda 呼び出しの制限に達したために，Lambda 関数呼び出しが失敗した場合，Kinesis Data Firehose は呼び出しをデフォルトで 3 回再試行する．

呼び出しが成功しなければ，Kinesis Data Firehose はそのレコードのバッチをスキップする．スキップされたレコードは処理失敗として扱われる．

`CreateDeliveryStream` または `UpdateDestination` API を使用して，再試行オプションを指定または上書きできる．このタイプの失敗の場合，呼び出しエラーログを Amazon CloudWatch Logs に出力できる．詳細については，「CloudWatch Logs を使用した Kinesis Data Firehose のモニタリング」を参照．

レコードのデータ変換のステータスが `ProcessingFailed` の場合，Kinesis Data Firehose はそのレコードを処理失敗として扱う．このタイプの失敗の場合，エラーログを Lambda 関数から Amazon CloudWatch Logs に出力できる．詳細については，AWS Lambda Developer Guideの「AWS Lambda の Amazon CloudWatch Logs へのアクセス」を参照．

データ変換が失敗した場合，処理に失敗したレコードは S3 バケットの processing-failed フォルダに配信されます。レコードの形式は以下のとおり．

- データ変換失敗時に S3 に吐かれるエラーログ（S3 のオブジェクト）

```json
{
    "attemptsMade": "count",
    "arrivalTimestamp": "timestamp",
    "errorCode": "code",
    "errorMessage": "message",
    "attemptEndingTimestamp": "timestamp",
    "rawData": "data",
    "lambdaArn": "arn"
}
```

- `attemptsMade`
  - 呼び出しリクエストの試行回数
- `arrivalTimestamp`
  - Kinesis Data Firehose がレコードを受信した時間
- `errorCode`
  - Lambda から返された HTTP エラーコード
- `errorMessage`
  - Lambda から返されたエラーメッセージ
- `attemptEndingTimestamp`
  - Kinesis Data Firehose が Lambda 呼び出しの試行を停止した時間
- `rawData`
  - base64 エンコード後のレコードデータ
- `lambdaArn`
  - Lambda 関数の Amazon リソースネーム (ARN)

### Lambda の呼び出し時間

Kinesis Data Firehose では，最大 5 分の Lambda 呼び出し時間がサポートされる．Lambda 関数の完了に 5 分を超える時間がかかる場合は，次のエラーが表示されます：

```txt
Firehose encountered timeout errors when calling AWS Lambda
（Firehose で，AWS Lambda を呼び出すときにタイムアウトエラーが発生しました）
```

サポートされている最大の関数タイムアウトは 5 分である．
このようなエラーが発生した場合の Kinesis Data Firehose による処理の詳細については，「データ変換失敗の処理」を参照してください。

### ソースレコードのバックアップ

Kinesis Data Firehose は，変換されたレコードを送信先に配信すると同時に，変換されなかった全てのレコードを S3 バケットにバックアップできる．ソースレコードのバックアップは，配信ストリームの作成または更新時に有効にすることができる．ソースレコードのバックアップは，有効にした後で無効にすることはできない．

### サブスクリプションフィルタ使うときの罠

デシリアライズするときの罠

- DynamoDB から送られてくるとき
  - base64 -> json string -> json
- CloudWatch Logs から送られてくるとき
  - base64 -> gzip string -> json string -> json
  - **gzip 圧縮されてる文字列を解凍する必要がある**
