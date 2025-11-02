"""
Lambda handler for deleting a user
DELETE /users/{userId}
"""
import json
import os
from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError

# Import utilities
try:
    from utils.response import success_response, not_found_response, bad_request_response, server_error_response
except ImportError:
    # Fallback for local development
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils.response import success_response, not_found_response, bad_request_response, server_error_response

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('USERS_TABLE', 'Users')
table = dynamodb.Table(table_name)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Delete a user from DynamoDB
    
    Args:
        event: API Gateway Lambda Proxy Input Format
        context: Lambda Context runtime methods and attributes
        
    Returns:
        API Gateway Lambda Proxy Output Format
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Extract userId from path parameters
        path_parameters = event.get('pathParameters', {})
        if not path_parameters or 'userId' not in path_parameters:
            return bad_request_response("Missing userId in path")
        
        user_id = path_parameters['userId']
        
        if not user_id or not user_id.strip():
            return bad_request_response("Invalid userId")
        
        # Check if user exists before deleting
        get_response = table.get_item(Key={'userId': user_id})
        if 'Item' not in get_response:
            return not_found_response(f"User with ID {user_id} not found")
        
        # Delete the user
        table.delete_item(Key={'userId': user_id})
        
        print(f"Successfully deleted user: {user_id}")
        
        return success_response({
            'message': f'User {user_id} deleted successfully',
            'userId': user_id
        })
        
    except ClientError as e:
        print(f"DynamoDB error: {str(e)}")
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        return server_error_response(f"Database error: {error_code} - {error_message}")
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return server_error_response(f"Internal server error: {str(e)}")
