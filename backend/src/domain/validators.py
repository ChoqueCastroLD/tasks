"""
Data validation functions for the task management system.

This module provides validation functions for task and user data,
ensuring that all data meets the required format and constraints.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import re
from uuid import UUID

from .exceptions import ValidationError

class TaskValidator:
    """Validator for Task entities."""
    
    @staticmethod
    def validate_title(title: str) -> None:
        """Validates the title of a task."""
        if not title:
            raise ValidationError("Title is required", {"title": "Title cannot be empty"})
        
        if len(title) < 3:
            raise ValidationError(
                "Title is too short",
                {"title": "Title must have at least 3 characters"}
            )
        
        if len(title) > 100:
            raise ValidationError(
                "Title is too long",
                {"title": "Title cannot exceed 100 characters"}
            )
    
    @staticmethod
    def validate_description(description: Optional[str]) -> None:
        """Validates the description of a task."""
        if description is not None:
            if len(description) > 500:
                raise ValidationError(
                    "Description is too long",
                    {"description": "Description cannot exceed 500 characters"}
                )
    
    @staticmethod
    def validate_status(status: Optional[str]) -> None:
        """Validates the status of a task."""
        if status is not None:
            valid_statuses = ["pending", "in_progress", "completed"]
            if status not in valid_statuses:
                raise ValidationError(
                    "Invalid status",
                    {"status": f"Status must be one of: {', '.join(valid_statuses)}"}
                )
    
    @staticmethod
    def validate_task_id(task_id: str) -> None:
        """Validates the task ID."""
        try:
            UUID(task_id)
        except ValueError:
            raise ValidationError(
                "Invalid task ID",
                {"task_id": "ID must be a valid UUID"}
            )
    
    @classmethod
    def validate_create_task(cls, data: Dict[str, Any]) -> None:
        """Validates data for creating a task."""
        if "title" not in data:
            raise ValidationError(
                "Missing required fields",
                {"title": "Title is required"}
            )
        
        if not isinstance(data.get("title"), str):
            raise ValidationError(
                "Invalid data type",
                {"title": "Title must be a string"}
            )
        
        if "description" in data and not isinstance(data["description"], str):
            raise ValidationError(
                "Invalid data type",
                {"description": "Description must be a string"}
            )
        
        if "status" in data and not isinstance(data["status"], str):
            raise ValidationError(
                "Invalid data type",
                {"status": "Status must be a string"}
            )
        
        cls.validate_title(data["title"])
        cls.validate_description(data.get("description"))
        cls.validate_status(data.get("status"))
    
    @classmethod
    def validate_update_task(cls, data: Dict[str, Any]) -> None:
        """Validates data for updating a task."""
        if not any(key in data for key in ["title", "description", "status"]):
            raise ValidationError(
                "No fields to update",
                {"body": "You must provide at least one field to update"}
            )
        
        if "title" in data and not isinstance(data["title"], str):
            raise ValidationError(
                "Invalid data type",
                {"title": "Title must be a string"}
            )
        
        if "description" in data and not isinstance(data["description"], str):
            raise ValidationError(
                "Invalid data type",
                {"description": "Description must be a string"}
            )
        
        if "status" in data and not isinstance(data["status"], str):
            raise ValidationError(
                "Invalid data type",
                {"status": "Status must be a string"}
            )
        
        if "title" in data:
            cls.validate_title(data["title"])
        if "description" in data:
            cls.validate_description(data["description"])
        if "status" in data:
            cls.validate_status(data["status"])


class AuthValidator:
    """Validator for authentication."""
    
    @staticmethod
    def validate_login_data(data: Dict[str, Any]) -> None:
        """
        Validate login data.
        
        Args:
            data: Dictionary containing login data
            
        Raises:
            ValidationError: If the data is invalid
        """
        if "username" not in data:
            raise ValidationError("Username is required")
        
        if "password" not in data:
            raise ValidationError("Password is required")
        
        if not isinstance(data["username"], str):
            raise ValidationError("Username must be a string")
        
        if not isinstance(data["password"], str):
            raise ValidationError("Password must be a string")
        
        if len(data["username"]) < 3:
            raise ValidationError("Username must be at least 3 characters long")
        
        if len(data["password"]) < 6:
            raise ValidationError("Password must be at least 6 characters long")
    
    @staticmethod
    def validate_registration_data(data: Dict[str, Any]) -> None:
        """Validates registration data."""
        if "username" not in data:
            raise ValidationError(
                "Missing required fields",
                {"username": "Username is required"}
            )
        
        if "password" not in data:
            raise ValidationError(
                "Missing required fields",
                {"password": "Password is required"}
            )
        
        if not isinstance(data["username"], str):
            raise ValidationError(
                "Invalid data type",
                {"username": "Username must be a string"}
            )
        
        if not isinstance(data["password"], str):
            raise ValidationError(
                "Invalid data type",
                {"password": "Password must be a string"}
            )
        
        if len(data["username"]) < 3:
            raise ValidationError(
                "Invalid username",
                {"username": "Username must have at least 3 characters"}
            )
        
        if len(data["password"]) < 6:
            raise ValidationError(
                "Invalid password",
                "Contraseña inválida",
                {"password": "La contraseña debe tener al menos 6 caracteres"}
            ) 