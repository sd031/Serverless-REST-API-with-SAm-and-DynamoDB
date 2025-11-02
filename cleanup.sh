#!/bin/bash

# Cleanup script to delete the CloudFormation stack and all resources

set -e

STACK_NAME="${STACK_NAME:-serverless-users-api}"
REGION="${AWS_REGION:-us-west-2}"

echo "🗑️  Deleting stack: $STACK_NAME in region: $REGION"
echo ""
echo "⚠️  WARNING: This will delete all resources including:"
echo "   - API Gateway"
echo "   - Lambda Functions"
echo "   - DynamoDB Table (and all data)"
echo "   - IAM Roles"
echo ""

read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Cleanup cancelled"
    exit 0
fi

echo ""
echo "🔄 Deleting CloudFormation stack..."

aws cloudformation delete-stack \
    --stack-name "$STACK_NAME" \
    --region "$REGION"

echo "⏳ Waiting for stack deletion to complete..."
aws cloudformation wait stack-delete-complete \
    --stack-name "$STACK_NAME" \
    --region "$REGION"

echo ""
echo "✅ Stack deleted successfully!"
echo "🧹 All resources have been cleaned up."
