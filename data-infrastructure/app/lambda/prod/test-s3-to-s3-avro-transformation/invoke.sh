aws lambda invoke \
  --function-name test-enjou-s3-to-s3-avro-transformation \
  --invocation-type Event \
  --payload fileb://event.json \
  output/outputfile.txt  # 関数の出力結果
