#!/bin/bash

# variables
Prefix="test-enjou-cfn"
BUCKET_NAME="${Prefix}-lambda-deploy-packages"
CFN_TEMPLATE="./template.yml"
CFN_TEMPLATE_PACKAGED="./template-packaged.yml"
CFN_STACK_NAME="test-lambda-cwl"
CHANGESET_OPTION=""

# upload Lambda deploy packages to S3
aws cloudformation package \
  --template-file "${CFN_TEMPLATE}" \
  --s3-bucket "${BUCKET_NAME}" \
  --output-template-file ${CFN_TEMPLATE_PACKAGED}

# IAM に関するリソースを作るときにこのオプションを扶養する必要がある（cf: https://github.com/aws/serverless-application-model/issues/51）
aws cloudformation deploy ${CHANGESET_OPTION} \
  --template "${CFN_TEMPLATE_PACKAGED}" \
  --stack-name "${CFN_STACK_NAME}" \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
  --parameter-overrides \
    Prefix="${Prefix}"
