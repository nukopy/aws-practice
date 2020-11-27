#!/bin/bash

CFN_STACK_NAME="test"

echo "deleting stack..."
aws cloudformation delete-stack \
--stack-name $CFN_STACK_NAME
echo "Done."
