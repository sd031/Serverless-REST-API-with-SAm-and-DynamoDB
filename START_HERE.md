# 🚀 START HERE - Serverless REST API with DynamoDB

Welcome! This is your complete guide to getting started with this serverless project.

## ⚡ Quick Deploy (5 Minutes)

```bash
# 1. Make scripts executable
chmod +x deploy.sh test-api.sh cleanup.sh

# 2. Deploy to AWS
./deploy.sh

# 3. Test your API (replace with your endpoint from step 2)
./test-api.sh https://YOUR_API_ENDPOINT
```

That's it! Your serverless API is live! 🎉

---

## 📖 Documentation Guide

### For First-Time Users
1. **START HERE** (you are here) - Quick start
2. **QUICKSTART.md** - Detailed setup guide
3. **README.md** - Main documentation

### For Understanding the System
4. **PROJECT_OVERVIEW.md** - Complete project overview
5. **ARCHITECTURE.md** - System architecture details
6. **API_EXAMPLES.md** - API usage examples

### For Development
- **src/handlers/** - Lambda function code
- **src/utils/** - Shared utilities
- **template.yaml** - Infrastructure definition

---

## 🎯 What You'll Build

A production-ready REST API with these endpoints:

```
POST   /users          → Create user
GET    /users          → List all users
GET    /users/{id}     → Get user by ID
PUT    /users/{id}     → Update user
DELETE /users/{id}     → Delete user
```

**Tech Stack**: API Gateway + Lambda + DynamoDB

---

## ✅ Prerequisites Checklist

Before deploying, ensure you have:

- [ ] **AWS Account** ([Sign up free](https://aws.amazon.com/free/))
- [ ] **AWS CLI** installed and configured
  ```bash
  aws --version
  aws configure  # If not configured
  ```
- [ ] **SAM CLI** installed
  ```bash
  sam --version
  # Install: brew install aws-sam-cli (macOS)
  ```
- [ ] **Python 3.9+** installed
  ```bash
  python3 --version
  ```

---

## 🚀 Deployment Steps

### Step 1: Verify Prerequisites
```bash
# Check all tools are installed
aws --version && sam --version && python3 --version
```

### Step 2: Configure AWS
```bash
aws configure
# Enter your AWS Access Key, Secret Key, and Region
```

### Step 3: Deploy
```bash
./deploy.sh
```

**First deployment** will ask:
- Stack Name: Press Enter (uses default)
- Region: Press Enter or specify (e.g., us-west-2)
- Confirm changes: Type `y`
- Allow IAM role creation: Type `y`
- Save configuration: Type `y`

Wait 2-3 minutes for deployment.

### Step 4: Get Your API Endpoint

After deployment, you'll see:
```
Outputs:
ApiEndpoint: https://abc123xyz.execute-api.us-west-2.amazonaws.com/Prod/
```

**Copy this URL!**

### Step 5: Test Your API

```bash
# Option 1: Use the test script
./test-api.sh https://YOUR_API_ENDPOINT

# Option 2: Manual test with curl
curl -X POST https://YOUR_API_ENDPOINT/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "age": 25}'
```

---

## 🎓 What's Included

### Code Files
- **5 Lambda Functions** (Python) - One for each CRUD operation
- **Validation & Response Utilities** - Reusable helper functions
- **SAM Template** - Infrastructure as Code

### Documentation
- **README.md** - Main documentation
- **QUICKSTART.md** - Detailed setup guide
- **ARCHITECTURE.md** - System design and architecture
- **API_EXAMPLES.md** - Complete API reference with examples
- **PROJECT_OVERVIEW.md** - Project summary and learning outcomes

### Tools & Scripts
- **deploy.sh** - One-command deployment
- **test-api.sh** - Automated API testing
- **cleanup.sh** - Remove all AWS resources
- **postman_collection.json** - Postman test collection

---

## 💡 Common Commands

```bash
# Deploy/Update the application
./deploy.sh

# Test the API
./test-api.sh https://YOUR_API_ENDPOINT

# View Lambda logs (replace function name)
aws logs tail /aws/lambda/CreateUser --follow

# Delete everything
./cleanup.sh
```

---

## 🎯 Learning Path

### Beginner
1. Deploy the application
2. Test all API endpoints
3. View CloudWatch logs
4. Explore AWS Console

### Intermediate
1. Modify Lambda functions
2. Add new validation rules
3. Customize error messages
4. Add new user fields

### Advanced
1. Add authentication (Cognito)
2. Implement pagination
3. Add caching layer
4. Set up CI/CD pipeline

---

## 📊 AWS Resources Created

When you deploy, AWS creates:

| Resource | Type | Purpose |
|----------|------|---------|
| Users | DynamoDB Table | Store user data |
| CreateUser | Lambda Function | Create users |
| GetUser | Lambda Function | Retrieve users |
| ListUsers | Lambda Function | List all users |
| UpdateUser | Lambda Function | Update users |
| DeleteUser | Lambda Function | Delete users |
| UsersAPI | API Gateway | REST API endpoints |
| IAM Roles | IAM | Lambda permissions |
| Log Groups | CloudWatch | Function logs |

---

## 💰 Cost Estimate

### Free Tier (First 12 months)
- ✅ 1M Lambda requests/month
- ✅ 1M API Gateway requests/month
- ✅ 25GB DynamoDB storage

### Beyond Free Tier
For 1 million requests/month: **~$5.45**

**You can test this project entirely within the free tier!**

---

## 🔧 Troubleshooting

### "SAM CLI not found"
```bash
# Install SAM CLI
brew install aws-sam-cli  # macOS
```

### "AWS credentials not configured"
```bash
aws configure
# Enter your AWS credentials
```

### "Stack already exists"
```bash
# Option 1: Delete existing stack
./cleanup.sh

# Option 2: Use different stack name
STACK_NAME=my-api ./deploy.sh
```

### "Permission denied" on scripts
```bash
chmod +x deploy.sh test-api.sh cleanup.sh
```

---

## 🎉 Success Indicators

You'll know it's working when:

1. ✅ Deployment completes without errors
2. ✅ You receive an API endpoint URL
3. ✅ Test script runs successfully
4. ✅ You can create/read/update/delete users
5. ✅ CloudWatch logs show function executions

---

## 🧹 Cleanup

When you're done:

```bash
./cleanup.sh
```

This removes **all AWS resources** and stops any charges.

⚠️ **Warning**: This deletes the DynamoDB table and all user data!

---

## 📚 Next Steps

After successful deployment:

1. **Explore the Code**
   - Read Lambda functions in `src/handlers/`
   - Understand validation logic in `src/utils/`

2. **Customize**
   - Add new user fields
   - Implement custom validation
   - Add business logic

3. **Enhance**
   - Add authentication
   - Implement search
   - Add pagination

4. **Learn More**
   - Read ARCHITECTURE.md
   - Study API_EXAMPLES.md
   - Explore AWS Console

---

## 🆘 Getting Help

### Documentation
- **QUICKSTART.md** - Detailed setup instructions
- **README.md** - Complete documentation
- **API_EXAMPLES.md** - API usage examples

### AWS Resources
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [AWS Support](https://aws.amazon.com/support/)

### Check Logs
```bash
# View Lambda function logs
aws logs tail /aws/lambda/CreateUser --follow
```

---

## ✨ Key Features

- ✅ **Serverless** - No servers to manage
- ✅ **Scalable** - Handles millions of requests
- ✅ **Cost-Effective** - Pay only for what you use
- ✅ **Production-Ready** - Error handling, validation, logging
- ✅ **Well-Documented** - Comprehensive guides
- ✅ **Easy to Deploy** - One command deployment
- ✅ **Easy to Clean Up** - One command cleanup

---

## 🎓 What You'll Learn

- ✅ AWS Lambda development
- ✅ API Gateway configuration
- ✅ DynamoDB operations
- ✅ Infrastructure as Code (SAM)
- ✅ Serverless architecture
- ✅ REST API design
- ✅ Error handling & validation
- ✅ AWS best practices

---

## 🚀 Ready to Start?

```bash
# Let's go!
./deploy.sh
```

**Good luck and happy building! 🎉**

---

## 📞 Quick Reference

| Action | Command |
|--------|---------|
| Deploy | `./deploy.sh` |
| Test | `./test-api.sh <endpoint>` |
| View Logs | `aws logs tail /aws/lambda/CreateUser --follow` |
| Cleanup | `./cleanup.sh` |
| List Stacks | `aws cloudformation list-stacks` |
| Describe Stack | `aws cloudformation describe-stacks --stack-name serverless-users-api` |

---

**Remember**: This entire project can run within AWS Free Tier! 🎁
