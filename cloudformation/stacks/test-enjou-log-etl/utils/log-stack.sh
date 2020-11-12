#!/bin/bash

if [ $# = 1 ]; then
  echo "logging stack..."
  # STACK_NAME="test-enjou-log-etl"
  STACK_NAME=$1

  aws cloudformation describe-stack-events --stack-name "${STACK_NAME}" > ./template/log.json

  echo "Done."
else
  echo "Please pass stack name."
  exit 1
fi
