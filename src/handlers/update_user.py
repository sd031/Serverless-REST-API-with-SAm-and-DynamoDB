"""
Lambda handler for updating a user
PUT /users/{userId}
"""
import json
import os
from datetime import datetime
from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError

# Import utilities
try:
    from utils.response import success_response, not_found_response, bad_request_response, server_error_response
    from utils.validation import validate_user_data, sanitize_user_data
except ImportError:
    # Fallback for local development
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils.response import success_response, not_found_response, bad_request_response, server_error_response
    from utils.validation import validate_user_data, sanitize_user_data

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('USERS_TABLE', 'Users')
table = dynamodb.Table(table_name)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Update a user in DynamoDB
    
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
        
        # Parse request body
        if not event.get('body'):
            return bad_request_response("Request body is required")
        
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return bad_request_response("Invalid JSON in request body")
        
        # Validate input data (no required fields for update)
        is_valid, error_message = validate_user_data(body)
        
        if not is_valid:
            return bad_request_response(error_message)
        
        # Check if user exists
        get_response = table.get_item(Key={'userId': user_id})
        if 'Item' not in get_response:
            return not_found_response(f"User with ID {user_id} not found")
        
        # Sanitize input data
        sanitized_data = sanitize_user_data(body)
        
        if not sanitized_data:
            return bad_request_response("No valid fields to update")
        
        # Build update expression
        update_expression = "SET updatedAt = :updatedAt"
        expression_attribute_values = {
            ':updatedAt': datetime.utcnow().isoformat() + 'Z'
        }
        
        if 'name' in sanitized_data:
            update_expression += ", #name = :name"
            expression_attribute_values[':name'] = sanitized_data['name']
        
        if 'email' in sanitized_data:
            update_expression += ", email = :email"
            expression_attribute_values[':email'] = sanitized_data['email']
        
        if 'age' in sanitized_data:
            update_expression += ", age = :age"
            expression_attribute_values[':age'] = sanitized_data['age']
        
        # Handle attribute name conflicts (name is a reserved keyword)
        expression_attribute_names = {}
        if 'name' in sanitized_data:
            expression_attribute_names['#name'] = 'name'
        
        # Update the user
        update_kwargs = {
            'Key': {'userId': user_id},
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_attribute_values,
            'ReturnValues': 'ALL_NEW'
        }
        
        if expression_attribute_names:
            update_kwargs['ExpressionAttributeNames'] = expression_attribute_names
        
        response = table.update_item(**update_kwargs)
        
        updated_user = response['Attributes']
        print(f"Successfully updated user: {user_id}")
        
        return success_response(updated_user)
        
    except ClientError as e:
        print(f"DynamoDB error: {str(e)}")
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        return server_error_response(f"Database error: {error_code} - {error_message}")
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return server_error_response(f"Internal server error: {str(e)}")
