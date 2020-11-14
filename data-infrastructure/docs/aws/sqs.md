# 非同期通信：メッセージキューイング

Amazon SQS / SNS について学んだ．

- [[AWS マイスターシリーズ]Amazon SQS / SNS](https://www2.slideshare.net/AmazonWebServicesJapan/aws-31275003)

## メッセージキューイングとは

- メッセージキューイング Message Queueing
  - 異なるソフトウェア間でデータを送受信する手法の一つで，直接データを渡すのではなく一旦第三者のソフトウェアに預けることで，送信側も受信側も好きなタイミングで送受信処理を行うことができるようにする方式．つまり，**ソフトウェアコンポーネント間の非同期型通信を提供する手法である**．
- メッセージキュー Message Queue，MQ
  - サーバ間，プロセス間，スレッド間での通信に使われるソフトウェアコンポーネント．メッセージキューイングを行うためのキューである．

```txt
Publisher ---> Message Queue <-- polling --> Subscriber
```

- ポイント
  - 送信側と受信側がメッセージキューに同時にやりとりしなくても良い
  - 受信側がメッセージを取り出すまで格納されたまま

## メッセージキューイングシステム

### Introduction

- **分割できないものはスケールできない**
  - スケールするには疎結合なアーキテクチャにする必要がある
  - 疎結合アーキテクチャには非同期処理が不可欠
  - 非同期処理の典型例がキューシステム
- 自分で高い耐障害性を持つキューシステムを作るのは困難

---

## Amazon SQS とは

- Amazon SQS（Simple Queue Service）
  - AWS フルマネージドな分散型キュー
- 特徴
  - 高い信頼性：複数のサーバ / データセンターにメッセージを保持
  - スケーラブル：多数の送信者 / 受信者に対応
  - 高スループット：メッセージが増加しても高スループットを出し続ける
    - スループット・・・単位時間あたりのデータ処理量
  - 低コスト：毎月の無料枠 + 使った分だけの従量課金

### SQS を使う利点

- SQS を使う利点
  - 疎結合 Loosely Coupled
    - これはそもそもメッセージキューイングシステム全般に言えること
    - サービスの連携部分（メッセージキューイングシステム（Pub/Sub システム）など）などは非常に重要でボトルネックになりやすい．例えば，Redis，RabbitMQ などはボトルネックになりやすい．
  - SQS はこのボトルネックになりやすい連携部分を，高い信頼性・高スケーラビリティ・高スループットのマネージド型のキューで解決する
  - Kinesis も似ている類だが，どちらかというとデータ基盤などにおけるデータ転送に重きを置いている．メッセージキューよりも高スループットでかつ，データ（SQS におけるメッセージ）の加工処理を行える．

<iframe src="//www.slideshare.net/slideshow/embed_code/key/8BW9w5JHA0n805?startSlide=9" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/AmazonWebServicesJapan/aws-black-belt-tech-amazon-sqs-amazon-sns" title="AWS Black Belt Tech シリーズ 2016 - Amazon SQS / Amazon SNS" target="_blank">AWS Black Belt Tech シリーズ 2016 - Amazon SQS / Amazon SNS</a> </strong> from <strong><a href="//www.slideshare.net/AmazonWebServicesJapan" target="_blank">Amazon Web Services Japan</a></strong> </div>

### SQS の特徴

- 高速
- 信頼性が⾼い
- 低コスト
- 分散マネージドキュー
- スケーラビリティに優れている
  - 複数の送信者と受信者に対応
  - メッセージが増加しても速度劣化しない
- 削除されなければ，メッセージはデフォルトで 4 ⽇日間保持される．保持期間を 60 秒から 14 ⽇の間で変更可能．
- 1 つのキューごとに最⼤ 120,000 通の Inﬂight メッセージ を保持．120,000 通を超えると OverLimit エラーとなる．
  - **Inflight メッセージ**：Visibility Timeout によって他から見えない状態のメッセージのこと
- 最⼤大メッセージサイズ：256 KB（ちなみに Amazon Kinesis Data Firehose は 1 MB）
- アクセスコントロールが可能

### SQS のコスト

- 無料利用枠
  - （SQS ご利用全ユーザ）毎月 100 万キューイングリクエストまで無料
- SQS リクエスト 100 万件につき 0.476 USD（※東京リージョン）
- 複数メッセージを 1 つのリクエストとしてバッチ送信することも可能
- データ転送
  - 送信（アウト）
    - 最初の 1 GB / 月：0 USD
    - 10 TB まで / 月：0.140 USD GB あたり 〜略〜
    - 次の 350 TB まで / 月：0.120 USD GB あたり
    - 350 TB を越える場合の価格は問い合わせ
    - **同一リージョン内の SQS と EC2 インスタンスのデータ転送は無料**

参考 URL： https://aws.amazon.com/jp/sqs/pricing/

---

### SQS で利用する識別子

参考 URL：[url](http://docs.aws.amazon.com/ja_jp/AWSSimpleQueueService/latest/SQSDeveloperGuide/ImportantIdentifiers.html)

- Queue URL（キュー URL）
  - キューを作成する際に払い出される URL
  - `https://sqs.[リージョン].amazonaws.com/[アカウントID]/[キュー名]`
- Message ID（メッセージ ID）
  - システムで割り当てられた ID（例：`0a41026d-283b-4e5c-9b3f-debffb709ef4`）
- Receipt Handle（受信ハンドル）
  - **メッセージ毎に固有の Receipt Handle を持つ**
  - **メッセージの削除や可視性（Visibility）の変更には，「受信ハンドル」を指定する必要がある**
  - メッセージを受信するたびに「受信ハンドル」も受信する
  - 同じメッセージでも，受信する度に異なる「受信ハンドル」を受け取る
  - このため，常に最新の受信ハンドルを使って削除等をすること

---

### SQS の機能の詳細

- Visibility Timeout 機能
- SQS Long Polling 機能
- Long Polling と Short Polling の 使い分けについて
- SQS Delay Queue 機能
- SQS Message Timers 機能
- SQS Dead Letter Queue 機能
- SQS Batch API actions
- Client Side Buﬀering および Request Batching

#### Visibility Timeout 機能

- 受信者がメッセージ受診後，他の受信者は一定時間（デフォルト 30 sec）そのメッセージを受信できない
  - **Inflight メッセージ**：Visibility Timeout によって他から見えない状態のメッセージのこと
- メッセージを削除しなければ，一定時間（デフォルト 30 sec）経過後，再度 1 名のみ，そのメッセージを受信できるようになる

#### SQS Long Polling 機能

- メッセージが有効になるまで待つことが出来る機能
  - タイムアウトがなければ，`ReceiveMessage` コールにより，最低 1 つ，または 1 コールで取得可能な最⼤大数のメッセージを取得可能（メッセージが存在する場合）
- 空もしくは取得失敗のレスポンスを削減可能
- `ReceiveMessage` コールの `WaitTimeSeconds` の値を変更することで Polling 可能
  - 0 ～ 20 秒の間

##### Long Polling と Short Polling の 使い分けについて

- 多くの場合は、Long Polling を推奨
  - 複数のキューを使う場合は，マルチスレッドで Polling する
- Short Polling を使う必要がある場合
  - `RecieveMessage` 呼び出し後，直ちに応答が必要な場合
    - e.g. 複数のキューを単⼀スレッドポーリングする場合，Long Polling タイムアウトするまで待機するため，処理が遅れてしまう．

<iframe src="//www.slideshare.net/slideshow/embed_code/key/LVVLAqZmy3r4ln?startSlide=25" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/AmazonWebServicesJapan/aws-31275003" title="[AWSマイスターシリーズ] Amazon SQS / SNS" target="_blank">[AWSマイスターシリーズ] Amazon SQS / SNS</a> </strong> from <strong><a href="//www.slideshare.net/AmazonWebServicesJapan" target="_blank">Amazon Web Services Japan</a></strong> </div>

#### SQS Delay Queue 機能

- キューに送られた新しいメッセージをある一定秒の間，見えなくすることが可能
  - 0 ～ 900 秒に設定可能
  - 設定すると，**そのキューに送信されるメッセージ全てに適⽤**
  - Visibility Timeout とは異なる
    - Visibility Timeout は受信後のメッセージが一定時間見えなくなる
    - Delay Queue は送信したメッセージが一定時間見えなくなる

`SendMessage` ---> Delay Queue ---> `ReceiveMessage` ---> Visibility Timeout

<iframe src="//www.slideshare.net/slideshow/embed_code/key/LVVLAqZmy3r4ln?startSlide=26" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/AmazonWebServicesJapan/aws-31275003" title="[AWSマイスターシリーズ] Amazon SQS / SNS" target="_blank">[AWSマイスターシリーズ] Amazon SQS / SNS</a> </strong> from <strong><a href="//www.slideshare.net/AmazonWebServicesJapan" target="_blank">Amazon Web Services Japan</a></strong> </div>

#### SQS Message Timers 機能

- **個々のメッセージ**が送信されてから⾒見見えるようになるまでの時間を設定可能
  - デフォルトは 0 秒。すぐ⾒見見えるようになる
  - キュー全体ではなく，**メッセージ単体に適⽤**
  - Message Timers が Delay Queue の遅延時間の設定を上書きする
  - Delay Queue はキュー全体のメッセージ，Message Timers はメッセージ単体という違い

#### SQS Dead Letter Queue 機能

- 指定回数受信されたメッセージが自動で別の Dead Letter Queue というキューに移動される機能
  - デフォルトは無効
  - 事前に作成したキューを Dead Letter Queue として指定する
  - ずっと未処理メッセージが残り続ける状況を回避するのに有効
    - メッセージが受信されてそれに基づいて Subscriber 側でタスクが実行されるが，タスクが失敗した場合はメッセージが消去されない．そのため，タスクが失敗し続けることによりメッセージが残り続ける問題を回避するために，Dead Letter Queue がある．
    - **受信したときに受信回数はインクリメントされるが，受診されたからと言って削除まで実行されるとは限らないという問題を回避**

#### SQS Batch API actions

- 1 コールで最⼤ 10 リクエスト処理が可能
  - `SendMessageBatch`
  - `DeleteMessageBatch`
  - `ChangeMessageVisibilityBatch`
- 通常メッセージ 1 通あたり 256KB まで送信可能
  - **注意**：`SendMessageBatch` シングルコールで送れるメッセージの合計サイズも 256KB まで

#### Client-side Buﬀering および Request Batching

- Client-side バッファが可能
  - `AmazonSQSBuﬀeredAsyncClient`
- 以下のリクエストをバッチに纏めることが可能
  - `SendMessage`
  - `DeleteMessage`
  - `ChangeMessageVisibility`
- 10 リクエストまでバッファ可能
- Batch リクエストとして送信するため，SQS へのリクエスト数を削減し，コスト削減が可能

### SQS のスケーリング

- SQS キューは高いスループットを提供できる
  - 秒間数千メッセージ
- 高いスループットを出す⽅法
  - Batch API により 1 度に 10 メッセージを処理する
  - 多くのメッセージ送信者と受信者を配置可能
    - AWS-SDK for Java ではデフォルト 50 コネクション
    - 以下のように `MaxConnections` の値を変更する

```java
AmazonSQS sqsClient = new AmazonSQSClient(
  credentials, new ClientConfiguration().withMaxConnections( producerCount + cousumerCount)
);
```

### SQS のアクセスコントロール

キューへのアクセスコントロールが可能．以下その例：

- 他の AWS アカウントに `SendMessage` のみ許可
- 特定の時間のみアクセス許可
- 特定の AWS アカウントのアクセスを拒否
- EC2 インスタンスからのアクセスのみ許可

```json
{
  "Version": "2012-11-05",
  "Id": "cd3ad3d9-2776-4ef1-a904-4c229d1642ee",
  "Statement": [
    {
      "Sid": "1",
      "Effect": "Allow",
      "Principal": { "aws": "111122223333" },
      "Action": ["sqs:SendMessage", "sqs:ReceiveMessage"],
      "Resource": "arn:aws:sqs:us-east-1:444455556666:queue2",
      "Condition": {
        "IpAddress": { "aws:SourceIp": "10.52.176.0/24" },
        "DateLessThan": { "aws:CurrentTime": "2009-06-30T12:00Z" }
      }
    }
  ]
}
```

### Amazon CloudWatch を使った SQS 監視

- 以下のメトリックスを利用可能

| メトリクス | 説明 |
| `NumberOfMessageSent` | キューに追加されたメッセージ数|
| `SentMessageSize` | キューに追加されたメッセージの合計サイズ|
| `NumberOfMessageReceived` | `ReceiveMessage` コールによって返されたメッセージ数|
| `NumberOfEmptyReceives` | `ReceiveMessage` によって返さなかったメッセージ数|
| `NumberOfMessagesDeleted` | キューから削除されたメッセージ数|
| `ApproximateNumberOfMessage` | Delayed Delay され，すぐに読み込みができなかったメッセージ数．Delay Queue またはメッセージ送信時の Delay 設定によるもの．|
| `ApproximateNumberOfMessage` | Visible キューから利用可能になったメッセージ数|
| `ApproximateNumberOfMessage` | NotVisible クライアントから送信されたが削除されていないか，visibility winodw の end まで到達していないメッセージ数|

### SQS ベストプラクティス

#### その 1

- 1 度のリクエストで複数のメッセージを送信または受信する方が速い
  - 最大 10 通まで
- 1 つのキューに対する送信者または受信者は複数立てた方が全体の処理速度が向上する
- 複数のキューに Long Polling するときには，キューごと に 1 スレッドを使う（複数キューにはマルチスレッド）
  - 最大 20 秒まで待つことができる

#### その 2

- 何度も同じメッセージを受信しても同じ結果になるように受信者側を実装する
  - SQS は最低 1 度のメッセージ到達を保証
  - 冪等性の担保？（「冪等性」の使い方あってる？）
- メッセージの受信順序が違ってても同じ結果になるように受信側を実装する
  - SQS はメッセージの順序を保証しない
- メッセージ受信側で Polling 処理を継続して実⾏するような仕組みの実装が必要
  - e.g. supervisord を使えば，複数プロセスで定期的に polling ができ，かつ，プロセスが落ちても⾃動で⽴ち上げてくれる

### SQS のメッセージにどんなデータを含めれば良いのか

- 例
  - ジョブ ID
  - イベント ID
  - ファイルパス
  - URI
- ⼤きなメッセージは S3 に保存，SQS にはそのポインター（オブジェクトの URL など）を載せる
  - 通常メッセージ 1 通あたり 256KB まで送信可能

### （重要）SQS 利用上の注意点

- 最低 1 度のメッセージ到達を保障
  - 2 度以上同じメッセージを受信することがある
    - **何回同じメッセージを受信しても同じ結果になるように実装する必要がある**（つまり，メッセージへの操作の冪等性を担保できるような実装にする）
- メッセージの順序は保障しない
  - 後に送ったメッセージが先に受信されることがある
    - **受信順序が違っても同じ結果になるように実装する**
  - キューの種類を設定できる：標準（順番を保証しない） or FIFO（順番を保証する）

---

### SQS の動作イメージ

1. メッセージの送信
2. メッセージの受信
3. 受信したメッセージの内容を元にタスク実行
4. タスクが無事完了したら，キューの中にある該当メッセージを消去

---

### SQS の始め方

- queue の作成
- 作成済みの queue 一覧
- 特定の queue へメッセージを送信
- 特定の queue からのメッセージを受信

#### queue の作成

```sh
# aws sqs create-queue --queue-name [queue name] --region [AWS region]
aws sqs create-queue --queue-name MyQueue --region ap-northeast-1
```

実行結果

```json
{
  "QueueUrl": "https://sqs.ap-northeast-1.amazonaws.com/[Account ID]/MyQueue"
}
```

#### 作成済みの queue 一覧

```sh
aws sqs list-queues
```

実行結果

```json
{
  "QueueUrls": [
    "https://sqs.ap-northeast-1.amazonaws.com/[Account ID]/MyQueue",
    "https://sqs.ap-northeast-1.amazonaws.com/[Account ID]/myque01"
  ]
}
```

#### 特定の queue へメッセージを送信

- メッセージの送信
  - Queue URL とメッセージボディを指定する必要がある

```sh
aws sqs send-message \
  --queue-url https://sqs.ap-northeast-1.amazonaws.com/[Account ID]/MyQueue \
  --message-body "THIS IS A TEST MESSAGE."
```

実行結果：ハッシュ化されたメッセージボディとメッセージ ID が返される

```json
{
  "MD5OfMessageBody": "32974e534f5f3d157d8e96dd419193be",
  "MessageId": "e48f09d6-08e1-4bf3-bfc5-0aeb1df7bceb"
}
```

#### 特定の queue からのメッセージを受信

```sh
aws sqs receive-message --queue-url https://sqs.ap-northeast-1.amazonaws.com/[Account ID]/MyQueue
```

実行結果

```json
{
  "Messages": [
    {
      "MessageId": "e48f09d6-08e1-4bf3-bfc5-0aeb1df7bceb",
      "ReceiptHandle": "AQEBP/yisMUtY977gdKRWY2kSMZPQBJPDYKUiocojEgj0jgeGbhYl+gMNVBYCJzaeSNfnTOycrCpIc0d2iH7/MY2nyX4fP/pwTA/pizY4cZeKK2eOOVaOzN7jdr2uFKZIUUq/ycCmF10+GZ0x/D/COMaEwOR2aJOBI+43IoC7H9ykAhRs4VLXIRyuqCJxelHQRsOd6mbCme64KEJuO98iyMpLK9kQbT4vASVdyh8Ux4qBRHUNESe2WPUNARDRHKGATb7tP/3UmsQyD3t+fv0wGg+R6YtCLAIAsTEKlU9ulqpEuMs9kZFxgBKCrOvltCcXtxanRGg0hg7t/LrZL/qgvew6XAmP4/YWJaoS+V/Vn5m1gerFsFqEGBL7KJDWB1JDKLED9ketsa2dvPp9jf/Xzw88g==",
      "MD5OfBody": "32974e534f5f3d157d8e96dd419193be",
      "Body": "THIS IS A TEST MESSAGE."
    }
  ]
}
```

#### 特定の queue の特定のメッセージを消去

```sh
aws sqs delete-message --queue-url [Queue URL] --receipt-handle [Receipt Handle]q2doVA==
aws sqs delete-message --queue-url https://sqs.us-east-1.amazonaws.com/80398EXAMPLE/MyQueue --receipt-handle AQEBRXTo[]q2doVA==
```

---

### AWS CLI で利用できる SQS のコマンド

command format: `aws sqs [command] [option]`

- `add-permission`
- `change-message-visibility`
- `change-message-visibility-batch`
- [x] `create-queue`
- `delete-message`
- `delete-message-batch`
- `delete-queue`
- `get-queue-attributes`
- `get-queue-url`
- `list-dead-letter-source-queues`
- `list-queue-tags`
- [x] `list-queues`
- `purge-queue`
- [x] `receive-message`
- `remove-permission`
- [x] `send-message`
- `send-message-batch`
- `set-queue-attributes`
- `tag-queue`
- `untag-queue`

#### delete-message

指定されたキュー（`QueueUrl`）から指定されたメッセージを削除する．
削除するメッセージを選択するには，メッセージの `ReceiptHandle` を使用する（メッセージ送信時に受け取る `MessageId` ではない）．

Amazon SQS では，たとえ Visibility Timeout（可視性タイムアウト）設定により他の受信者によりメッセージがロックされていても，キューからメッセージを消去できる．
Amazon SQS はキューに設定された Retension Time Period（メッセージ保持時間）を超えてキューに残っているメッセージを自動消去する．
