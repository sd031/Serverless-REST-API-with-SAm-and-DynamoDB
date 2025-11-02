"""
Input validation utilities for user data
"""
import re
from typing import Dict, List, Optional, Any


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_name(name: str) -> bool:
    """
    Validate name format
    
    Args:
        name: Name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    
    # Name should be 1-100 characters
    return 1 <= len(name.strip()) <= 100


def validate_age(age: Any) -> bool:
    """
    Validate age value
    
    Args:
        age: Age to validate
        
    Returns:
        True if valid, False otherwise
    """
    if age is None:
        return True  # Age is optional
    
    try:
        age_int = int(age)
        return 0 < age_int <= 150
    except (ValueError, TypeError):
        return False


def validate_user_data(data: Dict[str, Any], required_fields: Optional[List[str]] = None) -> tuple[bool, Optional[str]]:
    """
    Validate user data for create/update operations
    
    Args:
        data: User data dictionary
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Invalid data format"
    
    # Check required fields
    if required_fields:
        for field in required_fields:
            if field not in data or data[field] is None:
                return False, f"Missing required field: {field}"
    
    # Validate name if present
    if 'name' in data:
        if not validate_name(data['name']):
            return False, "Invalid name: must be 1-100 characters"
    
    # Validate email if present
    if 'email' in data:
        if not validate_email(data['email']):
            return False, "Invalid email format"
    
    # Validate age if present
    if 'age' in data:
        if not validate_age(data['age']):
            return False, "Invalid age: must be between 1 and 150"
    
    return True, None


def sanitize_user_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize and clean user data
    
    Args:
        data: User data dictionary
        
    Returns:
        Sanitized data dictionary
    """
    sanitized = {}
    
    if 'name' in data and data['name']:
        sanitized['name'] = str(data['name']).strip()
    
    if 'email' in data and data['email']:
        sanitized['email'] = str(data['email']).strip().lower()
    
    if 'age' in data and data['age'] is not None:
        try:
            sanitized['age'] = int(data['age'])
        except (ValueError, TypeError):
            pass
    
    return sanitized
