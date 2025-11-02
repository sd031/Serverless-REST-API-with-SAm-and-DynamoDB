# API Examples & Response Formats

This document provides detailed examples of API requests and responses.

## Base URL

```
https://YOUR_API_ID.execute-api.REGION.amazonaws.com/Prod
```

Replace `YOUR_API_ID` and `REGION` with your actual values.

---

## 1. Create User

### Request

```http
POST /users HTTP/1.1
Host: YOUR_API_ID.execute-api.us-west-2.amazonaws.com
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30
}
```

### cURL Example

```bash
curl -X POST https://YOUR_API_ENDPOINT/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30
  }'
```

### Success Response (201 Created)

```json
{
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T10:30:00.000Z"
}
```

### Error Response (400 Bad Request)

```json
{
  "error": "Invalid email format"
}
```

### Validation Rules

- **name**: Required, 1-100 characters
- **email**: Required, valid email format
- **age**: Optional, integer between 1-150

---

## 2. Get User by ID

### Request

```http
GET /users/123e4567-e89b-12d3-a456-426614174000 HTTP/1.1
Host: YOUR_API_ID.execute-api.us-west-2.amazonaws.com
```

### cURL Example

```bash
curl https://YOUR_API_ENDPOINT/users/123e4567-e89b-12d3-a456-426614174000
```

### Success Response (200 OK)

```json
{
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T10:30:00.000Z"
}
```

### Error Response (404 Not Found)

```json
{
  "error": "User with ID 123e4567-e89b-12d3-a456-426614174000 not found"
}
```

---

## 3. List All Users

### Request

```http
GET /users HTTP/1.1
Host: YOUR_API_ID.execute-api.us-west-2.amazonaws.com
```

### cURL Example

```bash
# Basic list
curl https://YOUR_API_ENDPOINT/users

# With limit
curl "https://YOUR_API_ENDPOINT/users?limit=10"

# With pagination
curl "https://YOUR_API_ENDPOINT/users?limit=10&lastKey=%7B%22userId%22%3A%22abc123%22%7D"
```

### Success Response (200 OK)

```json
{
  "users": [
    {
      "userId": "123e4567-e89b-12d3-a456-426614174000",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "age": 30,
      "createdAt": "2024-01-15T10:30:00.000Z",
      "updatedAt": "2024-01-15T10:30:00.000Z"
    },
    {
      "userId": "987f6543-e21c-34d5-b678-123456789abc",
      "name": "Jane Smith",
      "email": "jane.smith@example.com",
      "age": 28,
      "createdAt": "2024-01-15T11:00:00.000Z",
      "updatedAt": "2024-01-15T11:00:00.000Z"
    }
  ],
  "count": 2,
  "hasMore": false
}
```

### Response with Pagination

```json
{
  "users": [
    {
      "userId": "123e4567-e89b-12d3-a456-426614174000",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "age": 30,
      "createdAt": "2024-01-15T10:30:00.000Z",
      "updatedAt": "2024-01-15T10:30:00.000Z"
    }
  ],
  "count": 1,
  "hasMore": true,
  "lastKey": {
    "userId": "123e4567-e89b-12d3-a456-426614174000"
  }
}
```

### Query Parameters

- **limit**: Maximum number of users to return (default: 100, max: 1000)
- **lastKey**: Pagination token from previous response (URL-encoded JSON)

---

## 4. Update User

### Request

```http
PUT /users/123e4567-e89b-12d3-a456-426614174000 HTTP/1.1
Host: YOUR_API_ID.execute-api.us-west-2.amazonaws.com
Content-Type: application/json

{
  "name": "John Smith",
  "age": 31
}
```

### cURL Example

```bash
curl -X PUT https://YOUR_API_ENDPOINT/users/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "age": 31
  }'
```

### Success Response (200 OK)

```json
{
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Smith",
  "email": "john.doe@example.com",
  "age": 31,
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T12:45:00.000Z"
}
```

### Error Response (404 Not Found)

```json
{
  "error": "User with ID 123e4567-e89b-12d3-a456-426614174000 not found"
}
```

### Update Rules

- All fields are optional
- Only provided fields will be updated
- Email validation applies if email is provided
- `updatedAt` timestamp is automatically updated

---

## 5. Delete User

### Request

```http
DELETE /users/123e4567-e89b-12d3-a456-426614174000 HTTP/1.1
Host: YOUR_API_ID.execute-api.us-west-2.amazonaws.com
```

### cURL Example

```bash
curl -X DELETE https://YOUR_API_ENDPOINT/users/123e4567-e89b-12d3-a456-426614174000
```

### Success Response (200 OK)

```json
{
  "message": "User 123e4567-e89b-12d3-a456-426614174000 deleted successfully",
  "userId": "123e4567-e89b-12d3-a456-426614174000"
}
```

### Error Response (404 Not Found)

```json
{
  "error": "User with ID 123e4567-e89b-12d3-a456-426614174000 not found"
}
```

---

## Error Responses

### 400 Bad Request

Invalid input data or missing required fields.

```json
{
  "error": "Missing required field: name"
}
```

### 404 Not Found

Resource not found.

```json
{
  "error": "User with ID abc123 not found"
}
```

### 500 Internal Server Error

Server-side error.

```json
{
  "error": "Internal server error: Database connection failed"
}
```

---

## Response Headers

All responses include these headers:

```http
Content-Type: application/json
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token
Access-Control-Allow-Methods: GET,POST,PUT,DELETE,OPTIONS
```

---

## HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST (create) |
| 400 | Bad Request | Invalid input, validation error |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server-side error |

---

## JavaScript/Node.js Example

```javascript
const API_BASE_URL = 'https://YOUR_API_ENDPOINT';

// Create user
async function createUser(userData) {
  const response = await fetch(`${API_BASE_URL}/users`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });
  return response.json();
}

// Get user
async function getUser(userId) {
  const response = await fetch(`${API_BASE_URL}/users/${userId}`);
  return response.json();
}

// List users
async function listUsers(limit = 100) {
  const response = await fetch(`${API_BASE_URL}/users?limit=${limit}`);
  return response.json();
}

// Update user
async function updateUser(userId, updates) {
  const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updates),
  });
  return response.json();
}

// Delete user
async function deleteUser(userId) {
  const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
    method: 'DELETE',
  });
  return response.json();
}

// Usage example
(async () => {
  // Create a user
  const newUser = await createUser({
    name: 'Alice Johnson',
    email: 'alice@example.com',
    age: 25,
  });
  console.log('Created:', newUser);

  // Get the user
  const user = await getUser(newUser.userId);
  console.log('Retrieved:', user);

  // Update the user
  const updated = await updateUser(newUser.userId, { age: 26 });
  console.log('Updated:', updated);

  // List all users
  const allUsers = await listUsers();
  console.log('All users:', allUsers);

  // Delete the user
  const deleted = await deleteUser(newUser.userId);
  console.log('Deleted:', deleted);
})();
```

---

## Python Example

```python
import requests
import json

API_BASE_URL = 'https://YOUR_API_ENDPOINT'

def create_user(user_data):
    """Create a new user"""
    response = requests.post(
        f'{API_BASE_URL}/users',
        json=user_data
    )
    return response.json()

def get_user(user_id):
    """Get a user by ID"""
    response = requests.get(f'{API_BASE_URL}/users/{user_id}')
    return response.json()

def list_users(limit=100):
    """List all users"""
    response = requests.get(
        f'{API_BASE_URL}/users',
        params={'limit': limit}
    )
    return response.json()

def update_user(user_id, updates):
    """Update a user"""
    response = requests.put(
        f'{API_BASE_URL}/users/{user_id}',
        json=updates
    )
    return response.json()

def delete_user(user_id):
    """Delete a user"""
    response = requests.delete(f'{API_BASE_URL}/users/{user_id}')
    return response.json()

# Usage example
if __name__ == '__main__':
    # Create a user
    new_user = create_user({
        'name': 'Bob Wilson',
        'email': 'bob@example.com',
        'age': 35
    })
    print('Created:', json.dumps(new_user, indent=2))
    
    user_id = new_user['userId']
    
    # Get the user
    user = get_user(user_id)
    print('Retrieved:', json.dumps(user, indent=2))
    
    # Update the user
    updated = update_user(user_id, {'age': 36})
    print('Updated:', json.dumps(updated, indent=2))
    
    # List all users
    all_users = list_users()
    print(f'Total users: {all_users["count"]}')
    
    # Delete the user
    deleted = delete_user(user_id)
    print('Deleted:', json.dumps(deleted, indent=2))
```

---

## Testing Tips

### 1. Use Environment Variables

```bash
export API_ENDPOINT="https://YOUR_API_ID.execute-api.us-west-2.amazonaws.com/Prod"

curl -X POST $API_ENDPOINT/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}'
```

### 2. Save User ID for Testing

```bash
# Create and save user ID
USER_ID=$(curl -s -X POST $API_ENDPOINT/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "email": "test@example.com"}' \
  | jq -r '.userId')

# Use the saved ID
curl $API_ENDPOINT/users/$USER_ID
```

### 3. Pretty Print JSON

```bash
curl $API_ENDPOINT/users | jq '.'
```

### 4. Check Response Status

```bash
curl -w "\nHTTP Status: %{http_code}\n" $API_ENDPOINT/users
```

---

## Rate Limiting

API Gateway default limits:
- **10,000 requests per second** (steady-state)
- **5,000 requests** (burst)

Contact AWS Support to increase limits if needed.

---

## Best Practices

1. **Always validate responses**: Check HTTP status codes
2. **Handle errors gracefully**: Implement retry logic for 5xx errors
3. **Use pagination**: For large datasets, use the `limit` and `lastKey` parameters
4. **Cache responses**: Cache GET requests when appropriate
5. **Implement timeouts**: Set reasonable timeout values for API calls
6. **Log requests**: Keep audit logs of API interactions
7. **Secure credentials**: Never hardcode API endpoints or credentials

---

## Support

For issues or questions:
- Check CloudWatch Logs for detailed error messages
- Review the Lambda function code in `src/handlers/`
- Consult AWS documentation: https://docs.aws.amazon.com/
