#!/bin/bash

STACK_NAME="test-lambda-cwl"

echo "deleting stack..."
aws cloudformation delete-stack --stack-name "${STACK_NAME}"
echo "Done."
