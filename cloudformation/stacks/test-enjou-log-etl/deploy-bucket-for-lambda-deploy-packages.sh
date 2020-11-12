#!/bin/bash

CHANGESET_OPTION="--no-execute-changeset"

if [ $# = 1 ] && [ $1 = "deploy" ]; then
  echo "deploy mode"
  CHANGESET_OPTION=""
fi

CFN_TEMPLATE="./template/template-bucket-for-lambda-deploy-packages.yml"
CFN_STACK_NAME="test-enjou-s3-bucket-deploy-packages"

# deploy
Prefix="test-enjou-cfn"

aws cloudformation deploy \
  --template "${CFN_TEMPLATE}" \
  --stack-name "${CFN_STACK_NAME}" \
  --parameter-overrides \
    Prefix="${Prefix}" \
  ${CHANGESET_OPTION}
