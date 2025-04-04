"""
API handlers for the Task Manager application.

This module contains the handler functions for all API endpoints, including authentication
and task management operations. Each handler follows a consistent pattern of validating
input, processing the request, and returning a standardized response.
"""

import json
from typing import Dict, Any, Optional
from http import HTTPStatus

from src.application.services import TaskServiceImpl
from src.infrastructure.repositories import MongoTaskRepository
from src.infrastructure.auth import JwtAuthService
from src.domain.models import Task
from src.domain.exceptions import (
    AuthenticationError, ValidationError,
    ResourceNotFoundError, DatabaseError
)
from src.domain.validators import TaskValidator, AuthValidator
from src.config import (
    MONGO_URI, DB_NAME, JWT_SECRET,
    JWT_ALGORITHM, JWT_EXPIRE_MINUTES,
    CORS_ORIGINS
)
from src.api.error_handler import handle_exceptions

task_repository = MongoTaskRepository(MONGO_URI, DB_NAME, "tasks")
task_service = TaskServiceImpl(task_repository)
auth_service = JwtAuthService()

def create_response(status_code: int, body: Any) -> Dict:
    """Creates a standardized HTTP response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": CORS_ORIGINS[0] if CORS_ORIGINS else "*",
            "Access-Control-Allow-Credentials": "true"
        },
        "body": json.dumps(body)
    }

def get_user_from_token(event: Dict) -> str:
    """Extracts and verifies the JWT token from the event."""
    auth_header = event.get("headers", {}).get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthenticationError("Missing or invalid authorization header")
    
    token = auth_header.split(" ")[1]
    payload = auth_service.verify_token(token)
    if not payload:
        raise AuthenticationError("Invalid or expired token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationError("Invalid token payload")
    
    return user_id

@handle_exceptions
def register(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle user registration.
    
    Args:
        event: Dictionary containing request data
        
    Returns:
        Dict containing the response with status code and body
    """
    data = json.loads(event["body"])
    validate_login_data(data)
    
    token = auth_service.register(data["username"], data["password"])
    return create_response(201, {"token": token})

@handle_exceptions
def login(event: Dict, context: Any) -> Dict:
    try:
        body = json.loads(event.get("body", "{}"))
        
        if not body.get("username") or not body.get("password"):
            return create_response(400, {"error": "Username and password are required"})
        
        token = auth_service.authenticate(body["username"], body["password"])
        if not token:
            return create_response(401, {"error": "Invalid credentials"})
        
        return create_response(200, {"token": token})
    except Exception as e:
        return create_response(500, {"error": str(e)})

@handle_exceptions
def get_tasks(event: Dict, context: Any) -> Dict:
    """Gets all tasks."""
    user_id = get_user_from_token(event)
    tasks = task_service.get_all_tasks()
    return create_response(HTTPStatus.OK, {"tasks": [task.to_dict() for task in tasks]})

@handle_exceptions
def get_task(event: Dict, context: Any) -> Dict:
    """Gets a specific task."""
    user_id = get_user_from_token(event)
    task_id = event["pathParameters"]["taskId"]
    
    TaskValidator.validate_task_id(task_id)
    
    task = task_service.get_task_by_id(task_id)
    if not task:
        raise ResourceNotFoundError("Task", task_id)
    
    return create_response(HTTPStatus.OK, task.to_dict())

@handle_exceptions
def create_task(event: Dict, context: Any) -> Dict:
    """Creates a new task."""
    user_id = get_user_from_token(event)
    body = json.loads(event.get("body", "{}"))
    
    TaskValidator.validate_create_task(body)
    
    task = task_service.create_task(
        title=body["title"],
        description=body.get("description", ""),
        status=body.get("status", "pending"),
        user_id=user_id
    )
    return create_response(HTTPStatus.CREATED, task.to_dict())

@handle_exceptions
def update_task(event: Dict, context: Any) -> Dict:
    """Updates an existing task."""
    user_id = get_user_from_token(event)
    task_id = event["pathParameters"]["taskId"]
    body = json.loads(event.get("body", "{}"))
    
    TaskValidator.validate_task_id(task_id)
    TaskValidator.validate_update_task(body)
    
    task = task_service.update_task(
        task_id=task_id,
        title=body.get("title"),
        description=body.get("description"),
        status=body.get("status")
    )
    
    if not task:
        raise ResourceNotFoundError("Task", task_id)
    
    return create_response(HTTPStatus.OK, task.to_dict())

@handle_exceptions
def delete_task(event: Dict, context: Any) -> Dict:
    """Deletes a task."""
    user_id = get_user_from_token(event)
    task_id = event["pathParameters"]["taskId"]
    
    TaskValidator.validate_task_id(task_id)
    
    success = task_service.delete_task(task_id)
    if not success:
        raise ResourceNotFoundError("Task", task_id)
    
    return create_response(HTTPStatus.NO_CONTENT, {}) 