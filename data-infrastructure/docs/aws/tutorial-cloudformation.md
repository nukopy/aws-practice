# Udemy：AWS Cloudformation チュートリアル

## CloudFormation とは

- AWS リソースのプロビジョニング自動化サービス

## CloudFormation のユースケース

- AWS リソースの構築を効率化したい
- 開発・テスト・本番環境で利用するインフラを標準化したい
- 毎回同じリソースやプロビジョニング設定を正確に利用したい
  - 環境構築の正確性，効率性，再現性
- ソフトウェアと同じように環境構成を管理したい
  - テンプレート（テキストファイル）で管理できる

## CloudFormation の機能

- 変更管理機能
  - **変更セット**
    - スタックの更新を行う際の概要のこと．稼働中のリソースの変更による影響度を確認するためのスタック
    - スタックの変更・更新は直接更新と変更セットの実行で可能
  - **ドリフト**
    - テンプレートによって展開した AWS リソースを展開後に変更した場合に，元テンプレートとの差分を検出するチェック機能
- **スタックセット**
  - 1 つのテンプレートを用いて，複数のアカウント，複数のリージョンに対してスタックを作成できる機能
- スタック間のリソース参照機能
  - 被参照テンプレートの参照値を「エクスポート」し値を抽出し，その後，参照を行いたいテンプレートの「インポート」によりリソース参照を行える．これにより複数のスタックを連携したインフラ構築が可能になる．
  - あるスタックでのリソースを他のスタックで使い回す
- CloudFormation デザイナーの活用
  - CloudFormation テンプレート作成用のツールである「デザイナー」

## テンプレートのセクション

- AWSTemplateFormatVersion（任意）
  - テンプレートの形式を指定する
  - 現在は `2010-09-09` のみ利用可能．テンプレートファイルのお作法として，とりあえず指定しておくようにする．
- Description（任意）
- Metadata（任意）
- Parameters（任意）
- Mappings（任意）
- Resources（必須）
- Outputs（任意）

### Resources

テンプレートにおいて唯一必須のセッション．スタックに含める、VPC や EC2 インスタンスや S3 バケットなどのリソースを宣言します。

公式ドキュメント：リソース

リソース部分の構文はこちら。

```yml
Resources:
  <Logical ID>:
    Type: <Resource type>
    Properties: <Set of properties...>
```

- Logical ID
  - テンプレート内で一意な ID
  - テンプレートの中で，他のリソースを参照する場合などは，この ID を利用する．また，スタックのリソース一覧にも，この ID でリソースが表示される．
- Resource type
  - 実際に作成するリソースのタイプ
  - 対応しているリソースタイプは [AWS リソースプロパティタイプのリファレンス](http://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)に一覧がある
- Resource properties
  - 各リソースの作成時に指定するプロパティ．リソースタイプによって利用できるプロパティは異なるため，公式ドキュメントとにらめっこしながら指定していく

### Resources にタグを指定したテンプレートファイルの例

例えば，リソースに命名するときは，タグのキーに Name を指定して，任意の名前を入力する．

```yml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  hamadaVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      Tags:
      - Key: Name
        Value: first-VPC
```

最小構成であれば，設定ファイルは非常にシンプルであることが分かる．

## tutorial：VPC にサブネットやルーティングテーブルやインターネットゲートウェイを構築する

先述した VPC の設定ファイルは非常にシンプルだが，VPC には他にも設定が必要なリソースがある．

- インターネットゲートウェイ
- サブネット
- ルーティングテーブル

これらを，VPC と合わせて作成するテンプレート例は以下のようになる．
構成図も合わせて貼っておく．
先ほどと同じ手順で実行して，うまく関連リソース作成されたら OK．

```yml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  FirstVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      Tags:
      - Key: Name
        Value: FirstVPC
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
      - Key: Name
        Value: FirstVPC-IGW
  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref FirstVPC
      InternetGatewayId: !Ref InternetGateway
  FrontendRouteTable:
    Type: AWS::EC2::RouteTable
    DependsOn: AttachGateway
    Properties:
      VpcId: !Ref FirstVPC
      Tags:
      - Key: Name
        Value: FirstVPC-FrontendRoute
  FrontendRoute:
    Type: AWS::EC2::Route
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref FrontendRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway
  FrontendSubnet:
    Type: AWS::EC2::Subnet
    DependsOn: AttachGateway
    Properties:
      CidrBlock: 10.0.1.0/24
      MapPublicIpOnLaunch: 'true'
      VpcId: !Ref FirstVPC
      Tags:
      - Key: Name
        Value: FirstVPC-FrontendSubnet
  FrontendSubnetRouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref FrontendSubnet
      RouteTableId: !Ref FrontendRouteTable
```
