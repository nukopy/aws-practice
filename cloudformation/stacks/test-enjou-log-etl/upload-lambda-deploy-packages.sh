#!/bin/bash

Prefix="test-enjou-cfn"
BUCKET_NAME="${Prefix}-lambda-deploy-packages"

aws cloudformation package \
  --template-file template.yml \
  --s3-bucket "${BUCKET_NAME}" \
  --output-template-file template-packaged.yml
