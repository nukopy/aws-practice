#!/bin/bash

# variables
CFN_STACK_NAME="test"
Prefix="${CFN_STACK_NAME}-cfn"
CFN_TEMPLATE="./template.yaml"

# deploy
CHANGESET_OPTION="--no-execute-changeset"
if [ $# = 1 ] && [ $1 = "deploy" ]; then
  echo "deploy mode"
  CHANGESET_OPTION=""
fi

# IAM に関するリソースを作るときに --capabilities オプションを扶養する必要がある（cf: https://github.com/aws/serverless-application-model/issues/51）
aws cloudformation deploy ${CHANGESET_OPTION} \
  --template "${CFN_TEMPLATE}" \
  --stack-name "${CFN_STACK_NAME}" \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
  --parameter-overrides \
    Prefix="${Prefix}"
