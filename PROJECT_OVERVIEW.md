# Serverless REST API with DynamoDB - Project Overview

## 🎯 Project Goal

Build a production-ready, serverless CRUD API for user management using AWS services:
- **API Gateway** for REST endpoints
- **Lambda** for serverless compute
- **DynamoDB** for NoSQL data storage

## 📚 Concepts Covered

### 1. **Amazon API Gateway**
- REST API creation and configuration
- Lambda proxy integration
- CORS configuration
- Request/response transformation
- API deployment and stages

### 2. **AWS Lambda**
- Serverless function development in Python
- Event-driven architecture
- Environment variables
- IAM roles and permissions
- CloudWatch logging

### 3. **Amazon DynamoDB**
- NoSQL database design
- Primary key structure (Partition Key)
- CRUD operations (PutItem, GetItem, Scan, UpdateItem, DeleteItem)
- On-demand billing mode
- Conditional writes

### 4. **Infrastructure as Code**
- AWS SAM (Serverless Application Model)
- CloudFormation templates
- Resource provisioning
- Stack management

### 5. **Best Practices**
- Input validation and sanitization
- Error handling
- Logging and monitoring
- Security (IAM, HTTPS)
- Code organization

## 🏗️ Architecture

```
Client → API Gateway → Lambda Functions → DynamoDB
                              ↓
                        CloudWatch Logs
```

## 📁 Project Structure

```
aws_project_5/
├── src/
│   ├── handlers/                 # Lambda function handlers
│   │   ├── create_user.py       # POST /users
│   │   ├── get_user.py          # GET /users/{userId}
│   │   ├── list_users.py        # GET /users
│   │   ├── update_user.py       # PUT /users/{userId}
│   │   └── delete_user.py       # DELETE /users/{userId}
│   └── utils/                    # Shared utilities
│       ├── response.py          # HTTP response helpers
│       └── validation.py        # Input validation
├── template.yaml                 # SAM/CloudFormation template
├── requirements.txt              # Python dependencies
├── deploy.sh                     # Deployment script
├── test-api.sh                   # API testing script
├── cleanup.sh                    # Resource cleanup script
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── ARCHITECTURE.md               # Architecture details
├── API_EXAMPLES.md               # API usage examples
├── postman_collection.json       # Postman test collection
├── .gitignore                    # Git ignore rules
└── samconfig.toml.example        # SAM config example
```

## 🚀 Features

### API Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| POST | /users | Create new user | 201 |
| GET | /users | List all users | 200 |
| GET | /users/{userId} | Get user by ID | 200 |
| PUT | /users/{userId} | Update user | 200 |
| DELETE | /users/{userId} | Delete user | 200 |

### User Data Model

```json
{
  "userId": "UUID (auto-generated)",
  "name": "string (required, 1-100 chars)",
  "email": "string (required, valid email)",
  "age": "number (optional, 1-150)",
  "createdAt": "ISO 8601 timestamp",
  "updatedAt": "ISO 8601 timestamp"
}
```

### Validation Rules

- **Name**: Required, 1-100 characters
- **Email**: Required, valid email format (RFC 5322)
- **Age**: Optional, integer between 1-150

### Error Handling

- 400: Bad Request (validation errors)
- 404: Not Found (resource doesn't exist)
- 500: Internal Server Error (unexpected errors)

## 🛠️ Technology Stack

### AWS Services
- **API Gateway**: REST API management
- **Lambda**: Serverless compute (Python 3.9)
- **DynamoDB**: NoSQL database
- **CloudWatch**: Logging and monitoring
- **IAM**: Access management
- **CloudFormation**: Infrastructure as Code

### Development Tools
- **AWS SAM CLI**: Build and deploy
- **Python 3.9**: Lambda runtime
- **boto3**: AWS SDK for Python
- **curl**: API testing
- **Postman**: API testing (optional)

## 📊 AWS Resources Created

When deployed, this project creates:

1. **DynamoDB Table**
   - Name: `Users`
   - Billing: Pay-per-request
   - Streams: Enabled

2. **Lambda Functions** (5 total)
   - CreateUser
   - GetUser
   - ListUsers
   - UpdateUser
   - DeleteUser

3. **API Gateway**
   - REST API with CORS
   - Stage: Prod
   - Logging enabled

4. **IAM Roles**
   - Lambda execution roles
   - DynamoDB access policies

5. **CloudWatch Log Groups**
   - One per Lambda function
   - Retention: Default (never expire)

## 💰 Cost Breakdown

### Free Tier (First 12 months)
- Lambda: 1M requests/month
- API Gateway: 1M requests/month
- DynamoDB: 25GB storage, 25 WCU, 25 RCU

### Estimated Monthly Cost (1M requests)
- Lambda: ~$0.20
- API Gateway: ~$3.50
- DynamoDB: ~$1.25
- CloudWatch: ~$0.50
- **Total**: ~$5.45/month

### Cost Optimization Tips
1. Use on-demand billing for unpredictable workloads
2. Optimize Lambda memory allocation
3. Implement caching for frequently accessed data
4. Set CloudWatch log retention policies
5. Monitor and set up billing alarms

## 🔒 Security Features

### Implemented
- ✅ HTTPS only (enforced by API Gateway)
- ✅ IAM roles with least privilege
- ✅ Input validation and sanitization
- ✅ CORS configuration
- ✅ CloudWatch audit logging
- ✅ No hardcoded credentials

### Recommended for Production
- 🔒 API key authentication
- 🔒 AWS Cognito user pools
- 🔒 Request throttling
- 🔒 AWS WAF integration
- 🔒 VPC endpoints
- 🔒 Encryption with customer-managed keys

## 📈 Scalability

### Automatic Scaling
- **Lambda**: Up to 1,000 concurrent executions (default)
- **DynamoDB**: Unlimited with on-demand mode
- **API Gateway**: 10,000 RPS (steady-state)

### Performance Characteristics
- **Latency**: ~50-200ms per request
- **Throughput**: Thousands of requests per second
- **Availability**: 99.95% SLA (multi-AZ)

## 🧪 Testing

### Local Testing
```bash
sam local start-api
curl http://localhost:3000/users
```

### Integration Testing
```bash
./test-api.sh https://YOUR_API_ENDPOINT
```

### Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 https://YOUR_API_ENDPOINT/users
```

## 📝 Deployment Steps

1. **Prerequisites**: AWS CLI, SAM CLI, Python 3.9
2. **Configure AWS**: `aws configure`
3. **Deploy**: `./deploy.sh`
4. **Test**: `./test-api.sh <API_ENDPOINT>`
5. **Monitor**: Check CloudWatch logs
6. **Cleanup**: `./cleanup.sh`

## 🎓 Learning Outcomes

After completing this project, you will understand:

1. **Serverless Architecture**
   - Event-driven design
   - Function as a Service (FaaS)
   - Managed services benefits

2. **AWS Services**
   - API Gateway configuration
   - Lambda function development
   - DynamoDB operations
   - IAM policies

3. **Infrastructure as Code**
   - SAM templates
   - CloudFormation stacks
   - Resource dependencies

4. **Best Practices**
   - Error handling
   - Input validation
   - Logging and monitoring
   - Security principles

5. **DevOps**
   - Automated deployment
   - Testing strategies
   - Resource cleanup

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: aws-actions/setup-sam@v1
      - run: sam build
      - run: sam deploy --no-confirm-changeset
```

## 🐛 Troubleshooting

### Common Issues

1. **Lambda timeout**
   - Increase timeout in template.yaml
   - Optimize database queries

2. **DynamoDB throttling**
   - Check provisioned capacity
   - Use exponential backoff

3. **CORS errors**
   - Verify CORS configuration
   - Check request headers

4. **Permission errors**
   - Review IAM policies
   - Check Lambda execution role

## 📚 Additional Resources

### Documentation
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)

### Tutorials
- [AWS Serverless Workshops](https://workshops.aws/)
- [Serverless Land](https://serverlessland.com/)

## 🚀 Next Steps

### Phase 1: Enhancements
- [ ] Add authentication (Cognito)
- [ ] Implement pagination
- [ ] Add search functionality
- [ ] Create admin endpoints

### Phase 2: Advanced Features
- [ ] Email notifications (SES)
- [ ] File uploads (S3)
- [ ] Real-time updates (WebSockets)
- [ ] Caching (ElastiCache)

### Phase 3: Production Ready
- [ ] Multi-region deployment
- [ ] Disaster recovery plan
- [ ] Automated testing
- [ ] CI/CD pipeline
- [ ] Custom domain
- [ ] API documentation (Swagger)

## 🤝 Contributing

To extend this project:

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - Feel free to use this project for learning and commercial purposes.

## 🎉 Conclusion

This project demonstrates a complete serverless application using AWS best practices. It's production-ready, scalable, and cost-effective. Use it as a foundation for building more complex serverless applications!

**Happy Building! 🚀**
