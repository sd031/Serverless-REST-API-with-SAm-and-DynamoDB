"""
HTTP response helper functions for API Gateway Lambda proxy integration
"""
import json
from typing import Any, Dict, Optional


def create_response(
    status_code: int,
    body: Any,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Create a standardized API Gateway response
    
    Args:
        status_code: HTTP status code
        body: Response body (will be JSON serialized)
        headers: Optional additional headers
        
    Returns:
        Dict formatted for API Gateway Lambda proxy integration
    """
    default_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    if headers:
        default_headers.update(headers)
    
    return {
        'statusCode': status_code,
        'headers': default_headers,
        'body': json.dumps(body, default=str)
    }


def success_response(body: Any, status_code: int = 200) -> Dict[str, Any]:
    """Create a success response (2xx)"""
    return create_response(status_code, body)


def error_response(message: str, status_code: int = 400) -> Dict[str, Any]:
    """Create an error response (4xx or 5xx)"""
    return create_response(status_code, {'error': message})


def not_found_response(message: str = "Resource not found") -> Dict[str, Any]:
    """Create a 404 Not Found response"""
    return error_response(message, 404)


def bad_request_response(message: str = "Bad request") -> Dict[str, Any]:
    """Create a 400 Bad Request response"""
    return error_response(message, 400)


def server_error_response(message: str = "Internal server error") -> Dict[str, Any]:
    """Create a 500 Internal Server Error response"""
    return error_response(message, 500)


def created_response(body: Any) -> Dict[str, Any]:
    """Create a 201 Created response"""
    return success_response(body, 201)


def no_content_response() -> Dict[str, Any]:
    """Create a 204 No Content response"""
    return create_response(204, {})
