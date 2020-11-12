# AWS CLI

クイックリファレンス

## プロファイルの設定

AWS CLI で AWS にアクセスする場合，IAM ユーザやロールではなく，「プロファイル」という単位でアクセスを行う．実際には，IAM ユーザに紐づくアクセスキー ID，シークレットキーを用いるため，IAM ユーザに付与されているポリシーが「プロファイル」のアクセスできる権限となる．

- デフォルトプロファイルの設定

```sh
aws configure
```

- デフォルト以外のプロファイルの設定
  - IAM ユーザのアクセスキー ID，シークレットキーが必要になる
  - このユーザに適切なポリシーがアタッチされていなければ，AWS CLI から AWS リソースへのアクセスは行えないため注意

```sh
aws configure --profile [PROFILE NAME]
aws configure --profile jxpress
```

## IAM

参考：[[個人メモ]IAM の情報をAWS CLIで確認する](https://qiita.com/isobecky74/items/92d35fa1d3063fe64dc4)

- IAM ユーザの権限
  - 例えば，プロファイルに使用したアクセスキーに紐づくユーザの権限を知りたい場合，以下のコマンドを実行する

```sh
aws iam list-attached-user-policies --user-name [IAM USERNAME]
aws iam list-attached-user-policies --user-name y.okuwaki@jxpress.net
```

以下，出力．もし上記コマンドで指定した IAM ユーザのキーペアが AWS CLI のプロファイルに使用されている場合，以下の出力が AWS CLI における AWS リソースへのアクセス権限となる．

```json
{
  "AttachedPolicies": [
    {
      "PolicyName": "AdministratorAccess",
      "PolicyArn": "arn:aws:iam::aws:policy/AdministratorAccess"
    }
  ]
}
```
