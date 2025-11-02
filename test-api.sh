#!/bin/bash

# Test script for the Users API
# Usage: ./test-api.sh <API_ENDPOINT> [API_KEY]

set -e

# Check if API endpoint is provided
if [ -z "$1" ]; then
    echo "Usage: ./test-api.sh <API_ENDPOINT> [API_KEY]"
    echo "Example: ./test-api.sh https://abc123.execute-api.us-west-2.amazonaws.com/Prod your-api-key"
    exit 1
fi

# Remove trailing slash from endpoint if present
API_ENDPOINT="${1%/}"
BASE_URL="${API_ENDPOINT}/users"
API_KEY="$2"

# Set up headers based on whether API key is provided
if [ -n "$API_KEY" ]; then
    AUTH_HEADER="x-api-key: $API_KEY"
    echo "🧪 Testing Users API at: $BASE_URL (with API Key)"
else
    AUTH_HEADER=""
    echo "🧪 Testing Users API at: $BASE_URL (no API Key)"
fi
echo ""

# Test 1: Create a user
echo "1️⃣  Testing CREATE USER (POST /users)..."
if [ -n "$API_KEY" ]; then
    CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL" \
        -H "Content-Type: application/json" \
        -H "$AUTH_HEADER" \
        -d '{
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": 30
        }')
else
    CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": 30
        }')
fi

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
if [ -n "$API_KEY" ]; then
    GET_RESPONSE=$(curl -s -H "$AUTH_HEADER" "$BASE_URL/$USER_ID")
else
    GET_RESPONSE=$(curl -s "$BASE_URL/$USER_ID")
fi
echo "Response: $GET_RESPONSE"
echo ""

# Test 3: List all users
echo "3️⃣  Testing LIST USERS (GET /users)..."
if [ -n "$API_KEY" ]; then
    LIST_RESPONSE=$(curl -s -H "$AUTH_HEADER" "$BASE_URL")
else
    LIST_RESPONSE=$(curl -s "$BASE_URL")
fi
echo "Response: $LIST_RESPONSE"
echo ""

# Test 4: Update the user
echo "4️⃣  Testing UPDATE USER (PUT /users/{userId})..."
if [ -n "$API_KEY" ]; then
    UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/$USER_ID" \
        -H "Content-Type: application/json" \
        -H "$AUTH_HEADER" \
        -d '{
            "name": "John Smith",
            "age": 31
        }')
else
    UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/$USER_ID" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "John Smith",
            "age": 31
        }')
fi
echo "Response: $UPDATE_RESPONSE"
echo ""

# Test 5: Delete the user
echo "5️⃣  Testing DELETE USER (DELETE /users/{userId})..."
if [ -n "$API_KEY" ]; then
    DELETE_RESPONSE=$(curl -s -X DELETE -H "$AUTH_HEADER" "$BASE_URL/$USER_ID")
else
    DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/$USER_ID")
fi
echo "Response: $DELETE_RESPONSE"
echo ""

# Test 6: Verify deletion
echo "6️⃣  Testing GET DELETED USER (should return 404)..."
if [ -n "$API_KEY" ]; then
    VERIFY_RESPONSE=$(curl -s -w "\nHTTP Status: %{http_code}" -H "$AUTH_HEADER" "$BASE_URL/$USER_ID")
else
    VERIFY_RESPONSE=$(curl -s -w "\nHTTP Status: %{http_code}" "$BASE_URL/$USER_ID")
fi
echo "Response: $VERIFY_RESPONSE"
echo ""

echo "✅ All tests completed!"
