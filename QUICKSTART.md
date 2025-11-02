# Quick Start Guide

Get your Serverless Users API up and running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:

```bash
# Check AWS CLI
aws --version
# Should show: aws-cli/2.x.x or higher

# Check AWS credentials
aws sts get-caller-identity
# Should show your AWS account info

# Check SAM CLI
sam --version
# Should show: SAM CLI, version 1.x.x or higher

# Check Python
python3 --version
# Should show: Python 3.9 or higher
```

If any command fails, install the missing tool:
- **AWS CLI**: https://aws.amazon.com/cli/
- **SAM CLI**: `brew install aws-sam-cli` (macOS)
- **Python**: `brew install python@3.9` (macOS)

## Step 1: Configure AWS Credentials

If not already configured:

```bash
aws configure
```

Enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-west-2`)
- Default output format: `json`

## Step 2: Deploy the Application

Make the deployment script executable and run it:

```bash
chmod +x deploy.sh
./deploy.sh
```

**First-time deployment** will prompt you for:
- Stack Name: Press Enter for default (`serverless-users-api`)
- AWS Region: Press Enter for default or enter your preferred region
- Confirm changes: `y`
- Allow IAM role creation: `y`
- Save configuration: `y`

Wait 2-3 minutes for deployment to complete.

## Step 3: Get Your API Endpoint

After deployment, you'll see output like:

```
Outputs:
ApiEndpoint: https://abc123xyz.execute-api.us-west-2.amazonaws.com/Prod/
```

**Save this URL!** You'll need it for testing.

## Step 4: Test Your API

### Option A: Using the Test Script

```bash
chmod +x test-api.sh
./test-api.sh https://YOUR_API_ENDPOINT
```

Replace `YOUR_API_ENDPOINT` with your actual endpoint from Step 3.

### Option B: Using curl

**Create a user:**
```bash
curl -X POST https://YOUR_API_ENDPOINT/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "age": 28
  }'
```

**List all users:**
```bash
curl https://YOUR_API_ENDPOINT/users
```

**Get a specific user:**
```bash
curl https://YOUR_API_ENDPOINT/users/USER_ID
```

**Update a user:**
```bash
curl -X PUT https://YOUR_API_ENDPOINT/users/USER_ID \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "age": 29
  }'
```

**Delete a user:**
```bash
curl -X DELETE https://YOUR_API_ENDPOINT/users/USER_ID
```

### Option C: Using Postman

1. Import `postman_collection.json` into Postman
2. Update the `base_url` variable with your API endpoint
3. Run the requests in order

## Step 5: View Logs (Optional)

Check Lambda function logs:

```bash
# List log groups
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/

# View recent logs for CreateUser function
aws logs tail /aws/lambda/CreateUser --follow
```

## Step 6: Monitor in AWS Console

1. Go to AWS Console
2. Navigate to CloudFormation → Stacks → `serverless-users-api`
3. Click on "Resources" tab to see all created resources
4. Click on any resource to view details

## Common Issues & Solutions

### Issue: "SAM CLI not found"
**Solution**: Install SAM CLI
```bash
brew install aws-sam-cli  # macOS
```

### Issue: "AWS credentials not configured"
**Solution**: Run `aws configure` and enter your credentials

### Issue: "Stack already exists"
**Solution**: Either delete the existing stack or use a different stack name
```bash
./cleanup.sh  # Delete existing stack
STACK_NAME=my-new-stack ./deploy.sh  # Deploy with new name
```

### Issue: "Insufficient permissions"
**Solution**: Ensure your AWS user has permissions for:
- CloudFormation
- Lambda
- API Gateway
- DynamoDB
- IAM (for role creation)
- CloudWatch Logs

### Issue: "Template validation failed"
**Solution**: Ensure you're in the project root directory
```bash
cd /Users/sandipdas/aws_project_5
sam validate
```

## Next Steps

✅ **You now have a working serverless API!**

### Learn More:
- Read `README.md` for detailed documentation
- Check `ARCHITECTURE.md` for system design
- Review Lambda function code in `src/handlers/`

### Customize:
- Modify validation rules in `src/utils/validation.py`
- Add new fields to the user model
- Implement authentication
- Add more endpoints

### Production Checklist:
- [ ] Enable API Gateway API keys
- [ ] Add AWS Cognito authentication
- [ ] Enable DynamoDB point-in-time recovery
- [ ] Set up CloudWatch alarms
- [ ] Configure custom domain name
- [ ] Enable AWS WAF
- [ ] Set up CI/CD pipeline

## Cleanup

When you're done testing and want to delete all resources:

```bash
chmod +x cleanup.sh
./cleanup.sh
```

This will delete:
- API Gateway
- All Lambda functions
- DynamoDB table (and all data)
- IAM roles
- CloudWatch log groups

**Warning**: This action cannot be undone!

## Getting Help

- **AWS Documentation**: https://docs.aws.amazon.com/
- **SAM Documentation**: https://docs.aws.amazon.com/serverless-application-model/
- **GitHub Issues**: Create an issue in your repository

## Success! 🎉

You've successfully deployed a production-ready serverless REST API!

Your API is now:
- ✅ Scalable (handles millions of requests)
- ✅ Cost-effective (pay only for what you use)
- ✅ Highly available (multi-AZ by default)
- ✅ Secure (IAM roles, HTTPS)
- ✅ Monitored (CloudWatch logs and metrics)
