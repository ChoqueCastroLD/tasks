"""
Error handling utilities for the API.

This module provides functions and decorators for handling exceptions
and creating standardized error responses.
"""

import json
from functools import wraps
from typing import Dict, Any, Callable
from http import HTTPStatus

from ..domain.exceptions import TaskManagerException

def create_error_response(message: str, error_type: str, status_code: int = 500,
                         details: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        message: The error message
        error_type: The type of error
        status_code: HTTP status code
        details: Optional additional error details
        
    Returns:
        Dict containing the formatted error response
    """
    response = {
        "error": {
            "message": message,
            "type": error_type
        }
    }
    
    if details:
        response["error"]["details"] = details
    
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        },
        "body": json.dumps(response)
    }

def handle_exceptions(func: Callable) -> Callable:
    """
    Decorator to handle exceptions in API handlers.
    
    Args:
        func: The handler function to wrap
        
    Returns:
        Wrapped function that handles exceptions
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TaskManagerException as e:
            return create_error_response(
                message=str(e),
                error_type=e.__class__.__name__,
                status_code=e.status_code,
                details=getattr(e, "errors", None)
            )
        except Exception as e:
            return create_error_response(
                message="An unexpected error occurred",
                error_type="InternalServerError",
                status_code=500
            )
    return wrapper 