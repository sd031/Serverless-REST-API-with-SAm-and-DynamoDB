"""
Lambda handler for creating a new user
POST /users
"""
import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError

# Import utilities
try:
    from utils.response import created_response, bad_request_response, server_error_response
    from utils.validation import validate_user_data, sanitize_user_data
except ImportError:
    # Fallback for local development
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils.response import created_response, bad_request_response, server_error_response
    from utils.validation import validate_user_data, sanitize_user_data

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('USERS_TABLE', 'Users')
table = dynamodb.Table(table_name)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Create a new user in DynamoDB
    
    Args:
        event: API Gateway Lambda Proxy Input Format
        context: Lambda Context runtime methods and attributes
        
    Returns:
        API Gateway Lambda Proxy Output Format
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Parse request body
        if not event.get('body'):
            return bad_request_response("Request body is required")
        
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return bad_request_response("Invalid JSON in request body")
        
        # Validate required fields
        required_fields = ['name', 'email']
        is_valid, error_message = validate_user_data(body, required_fields)
        
        if not is_valid:
            return bad_request_response(error_message)
        
        # Sanitize input data
        sanitized_data = sanitize_user_data(body)
        
        # Generate user ID and timestamps
        user_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Create user item
        user_item = {
            'userId': user_id,
            'name': sanitized_data['name'],
            'email': sanitized_data['email'],
            'createdAt': timestamp,
            'updatedAt': timestamp
        }
        
        # Add optional age field
        if 'age' in sanitized_data:
            user_item['age'] = sanitized_data['age']
        
        # Save to DynamoDB
        table.put_item(Item=user_item)
        
        print(f"Successfully created user: {user_id}")
        
        return created_response(user_item)
        
    except ClientError as e:
        print(f"DynamoDB error: {str(e)}")
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        return server_error_response(f"Database error: {error_code} - {error_message}")
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return server_error_response(f"Internal server error: {str(e)}")
