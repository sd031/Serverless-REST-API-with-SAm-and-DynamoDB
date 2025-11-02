# API Security Documentation

## Overview

The Users API is secured with **API Key authentication** to prevent unauthorized access. All endpoints require a valid API key to be included in the request headers.

## Security Features

### 1. API Key Authentication
- **All endpoints require authentication** via API key
- API keys are managed through AWS API Gateway
- Keys are associated with usage plans for rate limiting and quotas

### 2. Rate Limiting & Throttling
- **Rate Limit**: 100 requests per second
- **Burst Limit**: 200 requests
- **Daily Quota**: 10,000 requests per day

These limits help prevent abuse and ensure fair usage across all API consumers.

### 3. CORS Configuration
- Configured to allow cross-origin requests
- Allows standard HTTP methods: GET, POST, PUT, DELETE, OPTIONS
- Includes necessary headers for API key authentication

## Getting Your API Key

After deploying the stack, retrieve your API key using the helper script:

```bash
./get-api-key.sh
```

Or manually via AWS CLI:

```bash
# Get the API Key ID from stack outputs
API_KEY_ID=$(aws cloudformation describe-stacks \
    --stack-name serverless-users-api \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiKeyId`].OutputValue' \
    --output text)

# Get the API Key value
aws apigateway get-api-key \
    --api-key "$API_KEY_ID" \
    --include-value \
    --query 'value' \
    --output text
```

## Using the API Key

### In cURL Requests

Include the API key in the `x-api-key` header:

```bash
curl -X GET "https://your-api-endpoint.com/Prod/users" \
  -H "x-api-key: your-api-key-here"
```

### In the Test Script

Pass the API key as the second argument:

```bash
./test-api.sh https://your-api-endpoint.com/Prod/ your-api-key-here
```

### In Application Code

#### JavaScript/Node.js
```javascript
const response = await fetch('https://your-api-endpoint.com/Prod/users', {
  headers: {
    'x-api-key': 'your-api-key-here',
    'Content-Type': 'application/json'
  }
});
```

#### Python
```python
import requests

headers = {
    'x-api-key': 'your-api-key-here',
    'Content-Type': 'application/json'
}

response = requests.get('https://your-api-endpoint.com/Prod/users', headers=headers)
```

#### Java
```java
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://your-api-endpoint.com/Prod/users"))
    .header("x-api-key", "your-api-key-here")
    .header("Content-Type", "application/json")
    .GET()
    .build();
```

## API Key Management

### Rotating API Keys

To rotate your API key for security:

1. Create a new API key in AWS Console or via CLI
2. Associate it with the usage plan
3. Update your applications with the new key
4. Delete the old key once migration is complete

```bash
# Create a new API key
aws apigateway create-api-key \
    --name "UsersAPIKey-New" \
    --enabled

# Associate with usage plan
aws apigateway create-usage-plan-key \
    --usage-plan-id <usage-plan-id> \
    --key-id <new-api-key-id> \
    --key-type API_KEY
```

### Disabling/Enabling Keys

```bash
# Disable a key
aws apigateway update-api-key \
    --api-key <api-key-id> \
    --patch-operations op=replace,path=/enabled,value=false

# Enable a key
aws apigateway update-api-key \
    --api-key <api-key-id> \
    --patch-operations op=replace,path=/enabled,value=true
```

## Error Responses

### 403 Forbidden - Missing or Invalid API Key

```json
{
  "message": "Forbidden"
}
```

**Causes:**
- API key not provided in request headers
- Invalid API key value
- API key is disabled
- API key not associated with the usage plan

### 429 Too Many Requests - Rate Limit Exceeded

```json
{
  "message": "Too Many Requests"
}
```

**Causes:**
- Exceeded rate limit (100 requests/second)
- Exceeded burst limit (200 requests)
- Exceeded daily quota (10,000 requests/day)

## Best Practices

### 1. Keep API Keys Secret
- ❌ Never commit API keys to version control
- ❌ Never expose API keys in client-side code
- ✅ Store API keys in environment variables
- ✅ Use secrets management services (AWS Secrets Manager, Parameter Store)

### 2. Use Environment Variables

```bash
# .env file (add to .gitignore)
API_KEY=your-api-key-here
API_ENDPOINT=https://your-api-endpoint.com/Prod/

# In your application
export API_KEY=$(cat .env | grep API_KEY | cut -d'=' -f2)
```

### 3. Implement Key Rotation
- Rotate API keys regularly (e.g., every 90 days)
- Have a process for emergency key rotation
- Keep audit logs of key usage

### 4. Monitor Usage
- Set up CloudWatch alarms for unusual activity
- Monitor rate limit violations
- Track API key usage patterns

### 5. Use Multiple Keys for Different Environments
- Separate keys for development, staging, and production
- Different keys for different applications/clients
- Easier to track and revoke access

## Additional Security Considerations

### Future Enhancements

Consider implementing these additional security measures:

1. **AWS IAM Authentication** - For internal/trusted applications
2. **Amazon Cognito** - For user-based authentication
3. **AWS WAF** - Web Application Firewall for advanced protection
4. **Request Signing** - AWS Signature Version 4 for request validation
5. **IP Whitelisting** - Restrict access to known IP addresses
6. **Custom Authorizers** - Lambda-based custom authentication logic

### Infrastructure Security

The API also benefits from:
- **DynamoDB Encryption** - Data encrypted at rest
- **API Gateway Logging** - CloudWatch logs for all requests
- **X-Ray Tracing** - Distributed tracing for debugging
- **IAM Roles** - Least privilege access for Lambda functions

## Compliance

This API implementation follows AWS best practices for:
- Data encryption in transit (HTTPS)
- Data encryption at rest (DynamoDB)
- Access control (API Keys + IAM)
- Audit logging (CloudWatch)
- Resource isolation (VPC-ready)

## Support

For security issues or questions:
1. Check CloudWatch logs for detailed error information
2. Review API Gateway execution logs
3. Verify API key is valid and enabled
4. Ensure usage plan limits haven't been exceeded

## References

- [AWS API Gateway API Keys](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-key-source.html)
- [API Gateway Usage Plans](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)
- [AWS Security Best Practices](https://docs.aws.amazon.com/security/)
