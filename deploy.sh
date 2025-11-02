#!/bin/bash

# Deployment script for Serverless Users API
# This script builds and deploys the SAM application

set -e  # Exit on error

echo "🚀 Starting deployment of Serverless Users API..."

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "❌ Error: AWS SAM CLI is not installed"
    echo "Please install it: brew install aws-sam-cli"
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ Error: AWS CLI is not configured"
    echo "Please run: aws configure"
    exit 1
fi

# Set default values
STACK_NAME="${STACK_NAME:-serverless-users-api}"
REGION="${AWS_REGION:-us-west-2}"

echo "📦 Building SAM application..."
sam build

echo "🔍 Validating template..."
sam validate

echo "☁️  Deploying to AWS..."
echo "   Stack Name: $STACK_NAME"
echo "   Region: $REGION"

# Deploy with guided mode if first time, otherwise use saved config
if [ -f "samconfig.toml" ]; then
    echo "   Using existing configuration from samconfig.toml"
    sam deploy
else
    echo "   Running guided deployment (first time setup)"
    echo ""
    echo "⚠️  IMPORTANT: When prompted for 'SAM configuration file', just press ENTER (don't type 'y')"
    echo ""
    sam deploy --guided \
        --stack-name "$STACK_NAME" \
        --region "$REGION" \
        --capabilities CAPABILITY_IAM \
        --no-fail-on-empty-changeset
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Stack Outputs:"
aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs' \
    --output table

echo ""
echo "🎉 Your API is ready to use!"
