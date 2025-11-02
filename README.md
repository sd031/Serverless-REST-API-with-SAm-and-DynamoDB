# Serverless REST API with DynamoDB

A complete **secured** serverless CRUD API for user management built with AWS Lambda, API Gateway, and DynamoDB. Features API key authentication, rate limiting, and comprehensive security controls.

## Architecture

- **API Gateway**: REST API endpoint
- **Lambda Functions**: Serverless compute for CRUD operations
- **DynamoDB**: NoSQL database for user data storage

## Features

### API Endpoints
- ✅ Create User (POST /users)
- ✅ Get User by ID (GET /users/{id})
- ✅ List All Users (GET /users)
- ✅ Update User (PUT /users/{id})
- ✅ Delete User (DELETE /users/{id})

### Security
- 🔐 API Key authentication on all endpoints
- 🛡️ Rate limiting (100 requests/second)
- 📊 Usage quotas (10,000 requests/day)
- 🔒 CORS configuration
- ✅ Input validation and sanitization

## Project Structure

```
.
├── src/
│   ├── handlers/
│   │   ├── create_user.py       # POST /users
│   │   ├── get_user.py          # GET /users/{id}
│   │   ├── list_users.py        # GET /users
│   │   ├── update_user.py       # PUT /users/{id}
│   │   └── delete_user.py       # DELETE /users/{id}
│   └── utils/
│       ├── response.py          # HTTP response helpers
│       └── validation.py        # Input validation
├── template.yaml                # SAM/CloudFormation template
├── requirements.txt             # Python dependencies
└── README.md
```

## Prerequisites

- AWS CLI configured with appropriate credentials
- AWS SAM CLI installed
- Python 3.9 or higher
- An AWS account

## Installation

1. **Install AWS SAM CLI** (if not already installed):
   ```bash
   brew install aws-sam-cli  # macOS
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Deployment

### Option 1: Using SAM CLI (Recommended)

1. **Build the application**:
   ```bash
   sam build
   ```

2. **Deploy the application**:
   ```bash
   sam deploy --guided
   ```
   
   Follow the prompts:
   - Stack Name: `serverless-users-api`
   - AWS Region: Your preferred region (e.g., `us-west-2`)
   - Confirm changes before deploy: `Y`
   - Allow SAM CLI IAM role creation: `Y`
   - Save arguments to configuration file: `Y`

3. **Note the outputs** from the deployment:
   ```
   Outputs:
   ApiEndpoint: https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/Prod/
   ApiKeyId: abcd1234efgh5678
   ```

4. **Retrieve your API Key**:
   ```bash
   ./get-api-key.sh
   ```
   
   This will display your API key value that you'll need for all API requests.

### Option 2: Using AWS CLI

```bash
# Package the application
sam package --output-template-file packaged.yaml --s3-bucket YOUR_S3_BUCKET

# Deploy the stack
sam deploy --template-file packaged.yaml --stack-name serverless-users-api --capabilities CAPABILITY_IAM
```

## API Usage

### Authentication

**All API endpoints require authentication via API key.** Include the API key in the `x-api-key` header with every request.

### Get Your API Key

After deployment, run:
```bash
./get-api-key.sh
```

Or manually:
```bash
API_KEY_ID=$(aws cloudformation describe-stacks \
    --stack-name serverless-users-api \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiKeyId`].OutputValue' \
    --output text)

aws apigateway get-api-key \
    --api-key "$API_KEY_ID" \
    --include-value \
    --query 'value' \
    --output text
```

### Base URL
```
https://YOUR_API_ID.execute-api.REGION.amazonaws.com/Prod
```

### 1. Create User
```bash
curl -X POST https://YOUR_API_ENDPOINT/users \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }'
```

**Response:**
```json
{
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "createdAt": "2024-01-01T12:00:00.000Z",
  "updatedAt": "2024-01-01T12:00:00.000Z"
}
```

### 2. Get User by ID
```bash
curl https://YOUR_API_ENDPOINT/users/123e4567-e89b-12d3-a456-426614174000 \
  -H "x-api-key: YOUR_API_KEY"
```

### 3. List All Users
```bash
curl https://YOUR_API_ENDPOINT/users \
  -H "x-api-key: YOUR_API_KEY"
```

**Response:**
```json
{
  "users": [
    {
      "userId": "123e4567-e89b-12d3-a456-426614174000",
      "name": "John Doe",
      "email": "john@example.com",
      "age": 30
    }
  ],
  "count": 1
}
```

### 4. Update User
```bash
curl -X PUT https://YOUR_API_ENDPOINT/users/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "name": "John Smith",
    "age": 31
  }'
```

### 5. Delete User
```bash
curl -X DELETE https://YOUR_API_ENDPOINT/users/123e4567-e89b-12d3-a456-426614174000 \
  -H "x-api-key: YOUR_API_KEY"
```

## Testing

### Automated Testing Script

Use the provided test script to test all endpoints:

```bash
# Get your API endpoint and key first
API_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name serverless-users-api \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
    --output text)

API_KEY=$(./get-api-key.sh | grep "API Key Value:" | cut -d' ' -f4)

# Run the test script
./test-api.sh $API_ENDPOINT $API_KEY
```

The test script will:
1. ✅ Create a new user
2. ✅ Retrieve the user by ID
3. ✅ List all users
4. ✅ Update the user
5. ✅ Delete the user
6. ✅ Verify deletion

### Testing Locally

1. **Start local API**:
   ```bash
   sam local start-api
   ```

2. **Test endpoints** (local testing doesn't require API key):
   ```bash
   # Create user
   curl -X POST http://localhost:3000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Test User", "email": "test@example.com", "age": 25}'
   
   # List users
   curl http://localhost:3000/users
   ```

## DynamoDB Table Schema

**Table Name**: `Users`

**Primary Key**:
- Partition Key: `userId` (String)

**Attributes**:
- `userId`: Unique identifier (UUID)
- `name`: User's full name (String)
- `email`: User's email address (String)
- `age`: User's age (Number, optional)
- `createdAt`: Timestamp of creation (String, ISO 8601)
- `updatedAt`: Timestamp of last update (String, ISO 8601)

## Monitoring

- **CloudWatch Logs**: Each Lambda function logs to CloudWatch
- **API Gateway Metrics**: Monitor request count, latency, and errors
- **DynamoDB Metrics**: Track read/write capacity and throttling

## Cleanup

To delete all resources:
```bash
sam delete --stack-name serverless-users-api
```

Or using AWS CLI:
```bash
aws cloudformation delete-stack --stack-name serverless-users-api
```

## Cost Optimization

- Lambda: Pay per request (free tier: 1M requests/month)
- DynamoDB: On-demand pricing (pay per request)
- API Gateway: Pay per API call (free tier: 1M calls/month)

## Security

### Implemented Security Features

- ✅ **API Key Authentication**: All endpoints require valid API key
- ✅ **Rate Limiting**: 100 requests/second, 200 burst limit
- ✅ **Usage Quotas**: 10,000 requests per day
- ✅ **IAM Roles**: Least privilege access for Lambda functions
- ✅ **Input Validation**: All user inputs are validated and sanitized
- ✅ **CORS Configuration**: Properly configured for web applications
- ✅ **Encryption**: Data encrypted at rest (DynamoDB) and in transit (HTTPS)
- ✅ **CloudWatch Logging**: All requests logged for audit

### API Key Management

**Retrieve API Key:**
```bash
./get-api-key.sh
```

**Rotate API Key:**
```bash
# Create new key
aws apigateway create-api-key --name "UsersAPIKey-New" --enabled

# Associate with usage plan
aws apigateway create-usage-plan-key \
    --usage-plan-id <usage-plan-id> \
    --key-id <new-api-key-id> \
    --key-type API_KEY

# Delete old key after migration
aws apigateway delete-api-key --api-key <old-api-key-id>
```

**Best Practices:**
- 🔐 Never commit API keys to version control
- 🔐 Store API keys in environment variables or secrets manager
- 🔐 Rotate API keys regularly (every 90 days)
- 🔐 Use different keys for different environments
- 🔐 Monitor API key usage in CloudWatch

For detailed security documentation, see [SECURITY.md](./SECURITY.md).

## Troubleshooting

### Issue: Lambda timeout
- Increase timeout in `template.yaml` (default: 30s)

### Issue: DynamoDB throttling
- Switch to provisioned capacity or increase on-demand limits

### Issue: CORS errors
- Update CORS configuration in `template.yaml`

### Issue: 403 Forbidden
- Verify API key is included in `x-api-key` header
- Check that API key is valid and enabled
- Ensure API key is associated with the usage plan

### Issue: 429 Too Many Requests
- You've exceeded rate limits or daily quota
- Wait for the rate limit window to reset
- Consider requesting higher limits if needed

## Project Files

- `template.yaml` - SAM/CloudFormation infrastructure template
- `src/handlers/` - Lambda function handlers
- `src/utils/` - Shared utility functions
- `test-api.sh` - Automated API testing script
- `get-api-key.sh` - Helper script to retrieve API key
- `deploy.sh` - Deployment automation script
- `cleanup.sh` - Resource cleanup script
- `SECURITY.md` - Detailed security documentation
- `API_EXAMPLES.md` - Additional API usage examples

## Next Steps

- ✅ ~~Add API key authentication~~ (Implemented)
- Add user authentication (AWS Cognito)
- Implement pagination for list operations
- Add data validation schemas (JSON Schema)
- Set up CI/CD pipeline (GitHub Actions/CodePipeline)
- Add comprehensive unit and integration tests
- Implement caching with ElastiCache or DynamoDB DAX
- Add request/response logging
- Implement API versioning

## License

MIT License
