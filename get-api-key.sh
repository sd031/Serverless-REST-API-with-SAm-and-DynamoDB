#!/bin/bash

# Script to retrieve the API Key value from AWS
# Usage: ./get-api-key.sh

set -e

echo "🔑 Retrieving API Key..."
echo ""

# Get the API Key ID from CloudFormation stack outputs
API_KEY_ID=$(aws cloudformation describe-stacks \
    --stack-name serverless-users-api \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiKeyId`].OutputValue' \
    --output text 2>/dev/null)

if [ -z "$API_KEY_ID" ]; then
    echo "❌ Could not find API Key ID in stack outputs"
    echo "Make sure the stack is deployed and the stack name is correct"
    exit 1
fi

echo "API Key ID: $API_KEY_ID"
echo ""

# Get the actual API Key value
API_KEY_VALUE=$(aws apigateway get-api-key \
    --api-key "$API_KEY_ID" \
    --include-value \
    --query 'value' \
    --output text 2>/dev/null)

if [ -z "$API_KEY_VALUE" ]; then
    echo "❌ Could not retrieve API Key value"
    exit 1
fi

echo "✅ API Key Value: $API_KEY_VALUE"
echo ""
echo "Use this key in your API requests with the header:"
echo "x-api-key: $API_KEY_VALUE"
echo ""
echo "Example test command:"
API_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name serverless-users-api \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
    --output text 2>/dev/null)

if [ -n "$API_ENDPOINT" ]; then
    echo "./test-api.sh $API_ENDPOINT $API_KEY_VALUE"
fi
