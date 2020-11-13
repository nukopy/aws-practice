#!/bin/bash

# variables
CFN_STACK_NAME="test-enjou-log-etl"
Prefix="${CFN_STACK_NAME}-cfn"
BUCKET_NAME="${Prefix}-s3-bucket-lambda-deploy-packages"
CFN_TEMPLATE="./template/template.yml"
CFN_TEMPLATE_PACKAGED="./template/template-packaged.yml"
# CFN_TEMPLATE="./templates/template.yml"
# CFN_TEMPLATE_PACKAGED="./templates/template-packaged.yml"
CHANGESET_OPTION=""

# upload Lambda deploy packages to S3
echo "Uploading Lambda deploy packages..."

aws cloudformation package \
  --template-file "${CFN_TEMPLATE}" \
  --s3-bucket "${BUCKET_NAME}" \
  --output-template-file ${CFN_TEMPLATE_PACKAGED}

echo "Done."

# deploy
CHANGESET_OPTION="--no-execute-changeset"
if [ $# = 1 ] && [ $1 = "deploy" ]; then
  echo "deploy mode"
  CHANGESET_OPTION=""
fi

# IAM に関するリソースを作るときに --capabilities オプションを扶養する必要がある（cf: https://github.com/aws/serverless-application-model/issues/51）
aws cloudformation deploy ${CHANGESET_OPTION} \
  --template "${CFN_TEMPLATE_PACKAGED}" \
  --stack-name "${CFN_STACK_NAME}" \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
  --parameter-overrides \
    Prefix="${Prefix}"
