"""
Lambda handler for listing all users
GET /users
"""
import json
import os
from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError

# Import utilities
try:
    from utils.response import success_response, server_error_response
except ImportError:
    # Fallback for local development
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils.response import success_response, server_error_response

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('USERS_TABLE', 'Users')
table = dynamodb.Table(table_name)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    List all users from DynamoDB
    
    Args:
        event: API Gateway Lambda Proxy Input Format
        context: Lambda Context runtime methods and attributes
        
    Returns:
        API Gateway Lambda Proxy Output Format
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Get query parameters for pagination (optional)
        query_params = event.get('queryStringParameters') or {}
        limit = int(query_params.get('limit', 100))
        
        # Ensure limit is reasonable
        if limit > 1000:
            limit = 1000
        
        # Scan the table
        scan_kwargs = {
            'Limit': limit
        }
        
        # Handle pagination token if provided
        if 'lastKey' in query_params:
            try:
                last_evaluated_key = json.loads(query_params['lastKey'])
                scan_kwargs['ExclusiveStartKey'] = last_evaluated_key
            except json.JSONDecodeError:
                pass  # Ignore invalid pagination token
        
        response = table.scan(**scan_kwargs)
        
        users = response.get('Items', [])
        
        # Prepare response
        result = {
            'users': users,
            'count': len(users)
        }
        
        # Add pagination info if there are more results
        if 'LastEvaluatedKey' in response:
            result['lastKey'] = response['LastEvaluatedKey']
            result['hasMore'] = True
        else:
            result['hasMore'] = False
        
        print(f"Successfully retrieved {len(users)} users")
        
        return success_response(result)
        
    except ClientError as e:
        print(f"DynamoDB error: {str(e)}")
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        return server_error_response(f"Database error: {error_code} - {error_message}")
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return server_error_response(f"Internal server error: {str(e)}")
