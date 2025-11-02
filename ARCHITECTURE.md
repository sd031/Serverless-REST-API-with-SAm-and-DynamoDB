# Architecture Documentation

## System Architecture

```
┌─────────────┐
│   Client    │
│ (Browser/   │
│  Mobile/    │
│  Postman)   │
└──────┬──────┘
       │
       │ HTTPS
       ▼
┌─────────────────────────────────────────┐
│         Amazon API Gateway              │
│  (REST API with CORS enabled)           │
│                                         │
│  Endpoints:                             │
│  • POST   /users                        │
│  • GET    /users                        │
│  • GET    /users/{userId}               │
│  • PUT    /users/{userId}               │
│  • DELETE /users/{userId}               │
└──────┬──────────────────────────────────┘
       │
       │ Invokes
       ▼
┌─────────────────────────────────────────┐
│         AWS Lambda Functions            │
│  (Python 3.9 Runtime)                   │
│                                         │
│  Functions:                             │
│  • CreateUser    - Create new user      │
│  • GetUser       - Get user by ID       │
│  • ListUsers     - List all users       │
│  • UpdateUser    - Update user info     │
│  • DeleteUser    - Delete user          │
│                                         │
│  Each function has:                     │
│  • 256 MB memory                        │
│  • 30 second timeout                    │
│  • IAM role with DynamoDB permissions   │
└──────┬──────────────────────────────────┘
       │
       │ Read/Write
       ▼
┌─────────────────────────────────────────┐
│         Amazon DynamoDB                 │
│  (NoSQL Database)                       │
│                                         │
│  Table: Users                           │
│  • Partition Key: userId (String)       │
│  • Billing: Pay-per-request             │
│  • Streams: Enabled                     │
│                                         │
│  Attributes:                            │
│  • userId (String, UUID)                │
│  • name (String)                        │
│  • email (String)                       │
│  • age (Number, optional)               │
│  • createdAt (String, ISO 8601)         │
│  • updatedAt (String, ISO 8601)         │
└─────────────────────────────────────────┘
       │
       │ Logs
       ▼
┌─────────────────────────────────────────┐
│       Amazon CloudWatch                 │
│  (Monitoring & Logging)                 │
│                                         │
│  • Lambda execution logs                │
│  • API Gateway access logs              │
│  • DynamoDB metrics                     │
│  • Custom metrics & alarms              │
└─────────────────────────────────────────┘
```

## Component Details

### 1. API Gateway

**Purpose**: Provides a RESTful HTTP interface for the application

**Features**:
- REST API with resource-based routing
- CORS enabled for cross-origin requests
- Request/response transformation
- Throttling and rate limiting
- API key management (optional)
- Request validation
- CloudWatch integration for logging

**Endpoints**:
| Method | Path | Lambda Function | Description |
|--------|------|----------------|-------------|
| POST | /users | CreateUser | Create a new user |
| GET | /users | ListUsers | List all users |
| GET | /users/{userId} | GetUser | Get user by ID |
| PUT | /users/{userId} | UpdateUser | Update user |
| DELETE | /users/{userId} | DeleteUser | Delete user |

### 2. Lambda Functions

**Purpose**: Serverless compute for business logic

**Common Configuration**:
- Runtime: Python 3.9
- Memory: 256 MB
- Timeout: 30 seconds
- Environment Variables:
  - `USERS_TABLE`: DynamoDB table name

**Function Details**:

#### CreateUser
- **Handler**: `create_user.lambda_handler`
- **Permissions**: DynamoDB PutItem
- **Validation**: Name (required), Email (required), Age (optional)
- **Response**: 201 Created with user object

#### GetUser
- **Handler**: `get_user.lambda_handler`
- **Permissions**: DynamoDB GetItem
- **Response**: 200 OK with user object or 404 Not Found

#### ListUsers
- **Handler**: `list_users.lambda_handler`
- **Permissions**: DynamoDB Scan
- **Features**: Pagination support with limit parameter
- **Response**: 200 OK with users array and count

#### UpdateUser
- **Handler**: `update_user.lambda_handler`
- **Permissions**: DynamoDB UpdateItem, GetItem
- **Validation**: At least one field to update
- **Response**: 200 OK with updated user object

#### DeleteUser
- **Handler**: `delete_user.lambda_handler`
- **Permissions**: DynamoDB DeleteItem, GetItem
- **Response**: 200 OK with confirmation message

### 3. DynamoDB Table

**Purpose**: Persistent data storage for user records

**Configuration**:
- Table Name: Users
- Primary Key: userId (Partition Key, String)
- Billing Mode: Pay-per-request (On-Demand)
- Point-in-time Recovery: Enabled (recommended for production)
- Encryption: AWS managed keys

**Access Patterns**:
1. **Create User**: PutItem with generated UUID
2. **Get User**: GetItem by userId
3. **List Users**: Scan operation (consider Query with GSI for production)
4. **Update User**: UpdateItem with conditional check
5. **Delete User**: DeleteItem with existence check

**Capacity Planning**:
- On-demand pricing scales automatically
- No capacity planning required
- Suitable for unpredictable workloads

### 4. IAM Roles & Permissions

**Lambda Execution Role**:
```yaml
Policies:
  - DynamoDBCrudPolicy (for Create, Update, Delete)
  - DynamoDBReadPolicy (for Get, List)
  - CloudWatchLogsFullAccess (for logging)
```

**Principle of Least Privilege**:
- Each Lambda function has only the permissions it needs
- Read-only functions cannot write to DynamoDB
- No cross-service permissions unless required

## Data Flow

### Create User Flow
```
1. Client sends POST /users with JSON body
2. API Gateway validates request format
3. API Gateway invokes CreateUser Lambda
4. Lambda validates input data
5. Lambda generates UUID and timestamps
6. Lambda writes to DynamoDB
7. DynamoDB confirms write
8. Lambda returns 201 with user object
9. API Gateway forwards response to client
```

### Get User Flow
```
1. Client sends GET /users/{userId}
2. API Gateway extracts userId from path
3. API Gateway invokes GetUser Lambda
4. Lambda queries DynamoDB by userId
5. DynamoDB returns item or empty
6. Lambda returns 200 with user or 404
7. API Gateway forwards response to client
```

## Security Considerations

### Current Implementation
- ✅ HTTPS only (enforced by API Gateway)
- ✅ IAM roles with least privilege
- ✅ Input validation and sanitization
- ✅ CORS configuration
- ✅ CloudWatch logging for audit trail

### Production Enhancements
- 🔒 Add API key authentication
- 🔒 Implement AWS Cognito for user authentication
- 🔒 Add request signing (AWS SigV4)
- 🔒 Enable AWS WAF for DDoS protection
- 🔒 Implement rate limiting per user
- 🔒 Add encryption at rest with customer-managed keys
- 🔒 Enable VPC endpoints for private access

## Scalability

### Automatic Scaling
- **Lambda**: Scales automatically up to account limits (1000 concurrent executions default)
- **DynamoDB**: On-demand mode scales automatically
- **API Gateway**: Handles 10,000 requests per second by default

### Performance Optimization
- Lambda warm-up strategies
- DynamoDB DAX for caching (if needed)
- API Gateway caching (if needed)
- Connection pooling in Lambda

## Monitoring & Observability

### CloudWatch Metrics
- Lambda invocations, duration, errors, throttles
- API Gateway request count, latency, 4xx/5xx errors
- DynamoDB read/write capacity, throttles

### CloudWatch Logs
- Lambda execution logs with request/response details
- API Gateway access logs
- Error traces and stack traces

### Alarms (Recommended)
- Lambda error rate > 5%
- API Gateway 5xx errors > 1%
- DynamoDB throttled requests > 0
- Lambda duration > 25 seconds

## Cost Estimation

### Monthly Cost (Approximate)
Assuming 1 million requests per month:

- **Lambda**: ~$0.20 (1M requests × 200ms avg × 256MB)
- **API Gateway**: ~$3.50 (1M requests)
- **DynamoDB**: ~$1.25 (1M writes + 1M reads)
- **CloudWatch**: ~$0.50 (logs)

**Total**: ~$5.45/month for 1M requests

### Free Tier Benefits
- Lambda: 1M free requests/month
- API Gateway: 1M free requests/month (first 12 months)
- DynamoDB: 25GB storage, 25 WCU, 25 RCU free forever

## Disaster Recovery

### Backup Strategy
- DynamoDB Point-in-Time Recovery (PITR)
- CloudFormation template in version control
- Lambda code in version control

### Recovery Procedures
1. Restore DynamoDB table from PITR
2. Redeploy Lambda functions from source
3. Recreate API Gateway from template

### RTO/RPO
- **RTO** (Recovery Time Objective): < 1 hour
- **RPO** (Recovery Point Objective): < 5 minutes (PITR)

## Future Enhancements

### Phase 2
- Add authentication with AWS Cognito
- Implement pagination for list operations
- Add search functionality with DynamoDB GSI
- Implement caching layer

### Phase 3
- Add email verification
- Implement user profile pictures (S3 integration)
- Add audit logging to separate table
- Implement soft deletes

### Phase 4
- Multi-region deployment
- GraphQL API option
- Real-time updates with WebSockets
- Advanced analytics with Kinesis
