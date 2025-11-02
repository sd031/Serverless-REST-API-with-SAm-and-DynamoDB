# Serverless REST API with DynamoDB

A complete serverless CRUD API for user management built with AWS Lambda, API Gateway, and DynamoDB.

## Architecture

- **API Gateway**: REST API endpoint
- **Lambda Functions**: Serverless compute for CRUD operations
- **DynamoDB**: NoSQL database for user data storage

## Features

- ✅ Create User (POST /users)
- ✅ Get User by ID (GET /users/{id})
- ✅ List All Users (GET /users)
- ✅ Update User (PUT /users/{id})
- ✅ Delete User (DELETE /users/{id})

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

3. **Note the API endpoint** from the output:
   ```
   Outputs:
   ApiEndpoint: https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/Prod/
   ```

### Option 2: Using AWS CLI

```bash
# Package the application
sam package --output-template-file packaged.yaml --s3-bucket YOUR_S3_BUCKET

# Deploy the stack
sam deploy --template-file packaged.yaml --stack-name serverless-users-api --capabilities CAPABILITY_IAM
```

## API Usage

### Base URL
```
https://YOUR_API_ID.execute-api.REGION.amazonaws.com/Prod
```

### 1. Create User
```bash
curl -X POST https://YOUR_API_ENDPOINT/users \
  -H "Content-Type: application/json" \
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
curl https://YOUR_API_ENDPOINT/users/123e4567-e89b-12d3-a456-426614174000
```

### 3. List All Users
```bash
curl https://YOUR_API_ENDPOINT/users
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
  -d '{
    "name": "John Smith",
    "age": 31
  }'
```

### 5. Delete User
```bash
curl -X DELETE https://YOUR_API_ENDPOINT/users/123e4567-e89b-12d3-a456-426614174000
```

## Testing Locally

1. **Start local API**:
   ```bash
   sam local start-api
   ```

2. **Test endpoints**:
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

## Security Best Practices

- ✅ IAM roles with least privilege
- ✅ API Gateway with throttling enabled
- ✅ Input validation on all endpoints
- ✅ CORS configuration for web applications
- 🔒 Consider adding API keys or Cognito authentication for production

## Troubleshooting

### Issue: Lambda timeout
- Increase timeout in `template.yaml` (default: 30s)

### Issue: DynamoDB throttling
- Switch to provisioned capacity or increase on-demand limits

### Issue: CORS errors
- Update CORS configuration in `template.yaml`

## Next Steps

- Add authentication (AWS Cognito)
- Implement pagination for list operations
- Add data validation schemas
- Set up CI/CD pipeline
- Add comprehensive unit and integration tests
- Implement caching with ElastiCache or DynamoDB DAX

## License

MIT License
