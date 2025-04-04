from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4, UUID

class Task:
    """Domain model for a task."""
    
    def __init__(
        self,
        title: str,
        description: str = "",
        status: str = "pending",
        task_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        created_by: Optional[str] = None
    ):
        """
        Initializes a task.
        
        Args:
            title: Task title
            description: Task description
            status: Task status (pending, in_progress, completed)
            task_id: Task ID (if not provided, a random one is generated)
            created_at: Creation date
            updated_at: Last update date
            created_by: ID of the user who created the task
        """
        self.task_id = task_id or str(uuid4())
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at
        self.created_by = created_by
    
    def update(self, title: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None) -> None:
        """
        Updates the task attributes.
        
        Args:
            title: New title
            description: New description
            status: New status
        """
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if status is not None:
            self.status = status
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the task to a dictionary.
        
        Returns:
            Dict with task data
        """
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "created_by": self.created_by
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Creates a Task instance from a dictionary.
        
        Args:
            data: Dictionary with task data
            
        Returns:
            Task instance
        """
        created_at = data.get("created_at")
        if created_at and isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
            
        updated_at = data.get("updated_at")
        if updated_at and isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
        
        return cls(
            task_id=data.get("task_id"),
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", "pending"),
            created_at=created_at,
            updated_at=updated_at,
            created_by=data.get("created_by")
        ) 