"""
Task service implementation.

This module provides the TaskService class which implements the business logic
for task management operations.
"""

from typing import List, Optional
from src.domain.interfaces import TaskService, TaskRepository
from src.domain.models import Task
from src.domain.exceptions import ResourceNotFoundError

class TaskServiceImpl(TaskService):
    """
    Implementation of the task service.
    
    This class implements the TaskService interface and provides the business logic
    for task management operations.
    """
    
    def __init__(self, task_repository: TaskRepository):
        """
        Initialize the task service.
        
        Args:
            task_repository: The repository to use for task storage
        """
        self.task_repository = task_repository
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.
        
        Returns:
            List of all tasks
        """
        return self.task_repository.get_all()
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            Task if found, None otherwise
        """
        return self.task_repository.get_by_id(task_id)
    
    def create_task(self, title: str, description: str, status: str, user_id: str) -> Task:
        """
        Create a new task.
        
        Args:
            title: The title of the task
            description: The description of the task
            status: The status of the task
            user_id: The ID of the user creating the task
            
        Returns:
            The created task
        """
        task = Task(
            title=title,
            description=description,
            status=status,
            created_by=user_id
        )
        return self.task_repository.save(task)
    
    def update_task(self, task_id: str, title: Optional[str] = None,
                   description: Optional[str] = None, status: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task.
        
        Args:
            task_id: The ID of the task to update
            title: Optional new title
            description: Optional new description
            status: Optional new status
            
        Returns:
            The updated task if found, None otherwise
        """
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ResourceNotFoundError("Task", task_id)
        
        task.update(
            title=title if title is not None else task.title,
            description=description if description is not None else task.description,
            status=status if status is not None else task.status
        )
        
        return self.task_repository.update(task)
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was deleted, False otherwise
        """
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ResourceNotFoundError("Task", task_id)
        
        return self.task_repository.delete(task_id) 