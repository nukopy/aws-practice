# CFn：AWS Lambda with CloudWatch Logs

CloudWatch Logs への書き込み権限を持つポリシーを作成する Lambda 関数にアタッチすれば，特にロググループを作る必要はなく，自動で Lambda 関数と CloudWatch Logs と連携される．

このテンプレートでは，Lambda の CloudWatch Logs への書き込み権限を与えるポリシーが記述されているが，実際には，AWS 側で用意されている `AWSLambdaBasicExecutionRole` というマネージドポリシーを使うことができる．

ここでは，テンプレート内で IAM ポリシーをリソースとして定義して，それをテンプレート内の IAM ロールにアタッチするという方法を試すために，わざわざポリシーを自作している．ポリシーの中身は `AWSLambdaBasicExecutionRole` と全く同じ．
