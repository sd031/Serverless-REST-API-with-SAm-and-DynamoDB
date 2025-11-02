#!/bin/bash

# Test script for the Users API
# Usage: ./test-api.sh <API_ENDPOINT>

set -e

# Check if API endpoint is provided
if [ -z "$1" ]; then
    echo "Usage: ./test-api.sh <API_ENDPOINT>"
    echo "Example: ./test-api.sh https://abc123.execute-api.us-west-2.amazonaws.com/Prod"
    exit 1
fi

# Remove trailing slash from endpoint if present
API_ENDPOINT="${1%/}"
BASE_URL="${API_ENDPOINT}/users"

echo "🧪 Testing Users API at: $BASE_URL"
echo ""

# Test 1: Create a user
echo "1️⃣  Testing CREATE USER (POST /users)..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30
    }')

echo "Response: $CREATE_RESPONSE"

# Extract userId using multiple methods for compatibility
if command -v jq &> /dev/null; then
    USER_ID=$(echo "$CREATE_RESPONSE" | jq -r '.userId')
else
    USER_ID=$(echo "$CREATE_RESPONSE" | grep -o '"userId"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"userId"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
fi

if [ -z "$USER_ID" ] || [ "$USER_ID" = "null" ]; then
    echo "❌ Failed to extract userId from response"
    exit 1
fi

echo "Created User ID: $USER_ID"
echo ""

# Wait a moment for consistency
sleep 1

# Test 2: Get the user by ID
echo "2️⃣  Testing GET USER (GET /users/{userId})..."
GET_RESPONSE=$(curl -s "$BASE_URL/$USER_ID")
echo "Response: $GET_RESPONSE"
echo ""

# Test 3: List all users
echo "3️⃣  Testing LIST USERS (GET /users)..."
LIST_RESPONSE=$(curl -s "$BASE_URL")
echo "Response: $LIST_RESPONSE"
echo ""

# Test 4: Update the user
echo "4️⃣  Testing UPDATE USER (PUT /users/{userId})..."
UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/$USER_ID" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "John Smith",
        "age": 31
    }')
echo "Response: $UPDATE_RESPONSE"
echo ""

# Test 5: Delete the user
echo "5️⃣  Testing DELETE USER (DELETE /users/{userId})..."
DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/$USER_ID")
echo "Response: $DELETE_RESPONSE"
echo ""

# Test 6: Verify deletion
echo "6️⃣  Testing GET DELETED USER (should return 404)..."
VERIFY_RESPONSE=$(curl -s -w "\nHTTP Status: %{http_code}" "$BASE_URL/$USER_ID")
echo "Response: $VERIFY_RESPONSE"
echo ""

echo "✅ All tests completed!"
