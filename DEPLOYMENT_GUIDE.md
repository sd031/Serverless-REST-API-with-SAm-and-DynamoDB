# Deployment Guide - Secured API

## Quick Start

### 1. Deploy the Stack

```bash
./deploy.sh
```

This will:
- Build the SAM application
- Deploy to AWS
- Create API Gateway with API key authentication
- Set up DynamoDB table
- Configure Lambda functions

### 2. Get Your API Key

After deployment completes, retrieve your API key:

```bash
./get-api-key.sh
```

**Save this API key securely!** You'll need it for all API requests.

### 3. Test the API

Run the automated test script:

```bash
# Get your endpoint from deployment output
API_ENDPOINT="https://YOUR_API_ID.execute-api.us-west-2.amazonaws.com/Prod/"
API_KEY="your-api-key-from-step-2"

./test-api.sh $API_ENDPOINT $API_KEY
```

## Deployment Outputs

After deployment, you'll see these outputs:

```
Outputs
----------------------------------------------------
Key                 ApiEndpoint
Description         API Gateway endpoint URL
Value               https://xxxxx.execute-api.us-west-2.amazonaws.com/Prod/

Key                 ApiKeyId
Description         API Key ID (use AWS CLI to get the actual key value)
Value               abcd1234efgh

Key                 UsersTableName
Description         DynamoDB table name
Value               Users

Key                 UsersTableArn
Description         DynamoDB table ARN
Value               arn:aws:dynamodb:us-west-2:xxxxx:table/Users
```

## Security Configuration

### API Key Settings

- **Rate Limit**: 100 requests/second
- **Burst Limit**: 200 requests
- **Daily Quota**: 10,000 requests/day

### How to Use API Key

Include in every request header:
```bash
curl -H "x-api-key: YOUR_API_KEY" https://YOUR_API_ENDPOINT/users
```

## Manual Deployment Steps

If you prefer manual deployment:

### 1. Build

```bash
sam build
```

### 2. Deploy

```bash
sam deploy --guided
```

Follow the prompts:
- **Stack Name**: `serverless-users-api`
- **AWS Region**: Your preferred region (e.g., `us-west-2`)
- **Confirm changes before deploy**: `Y`
- **Allow SAM CLI IAM role creation**: `Y`
- **Save arguments to configuration file**: `Y`

### 3. Retrieve API Key

```bash
# Get API Key ID
API_KEY_ID=$(aws cloudformation describe-stacks \
    --stack-name serverless-users-api \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiKeyId`].OutputValue' \
    --output text)

# Get API Key Value
aws apigateway get-api-key \
    --api-key "$API_KEY_ID" \
    --include-value \
    --query 'value' \
    --output text
```

## Environment-Specific Deployments

### Development Environment

```bash
sam deploy \
    --stack-name serverless-users-api-dev \
    --parameter-overrides Environment=dev
```

### Production Environment

```bash
sam deploy \
    --stack-name serverless-users-api-prod \
    --parameter-overrides Environment=prod
```

## Updating the Stack

To update after making changes:

```bash
./deploy.sh
```

Or manually:

```bash
sam build
sam deploy
```

**Note**: API keys persist across updates. You don't need to retrieve them again unless you rotate them.

## Rollback

If deployment fails or you need to rollback:

```bash
aws cloudformation cancel-update-stack --stack-name serverless-users-api
```

Or delete and redeploy:

```bash
sam delete --stack-name serverless-users-api
./deploy.sh
```

## Monitoring Deployment

### Check Stack Status

```bash
aws cloudformation describe-stacks \
    --stack-name serverless-users-api \
    --query 'Stacks[0].StackStatus' \
    --output text
```

### View Stack Events

```bash
aws cloudformation describe-stack-events \
    --stack-name serverless-users-api \
    --max-items 10
```

### Check Lambda Functions

```bash
aws lambda list-functions \
    --query 'Functions[?starts_with(FunctionName, `CreateUser`) || starts_with(FunctionName, `GetUser`)].FunctionName'
```

## Troubleshooting Deployment

### Issue: Stack already exists

```bash
# Update existing stack
sam deploy

# Or delete and recreate
sam delete --stack-name serverless-users-api
./deploy.sh
```

### Issue: Insufficient permissions

Ensure your AWS credentials have these permissions:
- CloudFormation: Full access
- Lambda: Create/update functions
- API Gateway: Create/update APIs
- DynamoDB: Create/update tables
- IAM: Create roles and policies

### Issue: S3 bucket not found

SAM creates a managed S3 bucket. If you see this error:

```bash
sam deploy --guided --resolve-s3
```

### Issue: API Key not found after deployment

Wait a few seconds for resources to be fully created, then:

```bash
./get-api-key.sh
```

## Post-Deployment Checklist

- [ ] Deployment completed successfully
- [ ] API endpoint is accessible
- [ ] API key retrieved and saved securely
- [ ] Test script runs successfully
- [ ] All CRUD operations work
- [ ] Rate limiting is enforced
- [ ] CloudWatch logs are being generated
- [ ] DynamoDB table is created

## Next Steps After Deployment

1. **Test the API** with the test script
2. **Set up monitoring** in CloudWatch
3. **Configure alarms** for errors and throttling
4. **Document your API key** in a secure location
5. **Share API endpoint** with your team (not the API key!)
6. **Set up CI/CD** for automated deployments

## Clean Up

To remove all resources:

```bash
./cleanup.sh
```

Or manually:

```bash
sam delete --stack-name serverless-users-api
```

**Warning**: This will delete:
- All Lambda functions
- API Gateway
- DynamoDB table (and all data!)
- CloudWatch logs
- IAM roles

## Support

For issues during deployment:
1. Check CloudFormation events in AWS Console
2. Review CloudWatch logs
3. Verify AWS credentials and permissions
4. Ensure SAM CLI is up to date: `sam --version`

## References

- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [API Gateway API Keys](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-key-source.html)
- [CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
