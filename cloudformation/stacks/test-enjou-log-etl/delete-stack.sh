#!/bin/bash

if [ $# = 1 ]; then
  echo "deleting stack..."
  aws cloudformation delete-stack \
  --stack-name $1
  echo "Done."
else
  echo "Please pass stack name."
  exit 1
fi
