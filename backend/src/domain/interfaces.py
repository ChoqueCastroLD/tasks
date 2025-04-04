from abc import ABC, abstractmethod
from typing import List, Optional

from .models import Task

class TaskRepository(ABC):
    """Interface for the task repository."""
    
    @abstractmethod
    def get_all(self) -> List[Task]:
        """Gets all tasks."""
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Gets a task by its ID."""
        pass
    
    @abstractmethod
    def save(self, task: Task) -> Task:
        """Saves a task."""
        pass
    
    @abstractmethod
    def update(self, task: Task) -> Task:
        """Updates a task."""
        pass
    
    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """Deletes a task by its ID."""
        pass

class TaskService(ABC):
    """Interface for the task service."""
    
    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        """Gets all tasks."""
        pass
    
    @abstractmethod
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Gets a task by its ID."""
        pass
    
    @abstractmethod
    def create_task(self, title: str, description: str, status: str, user_id: str) -> Task:
        """Creates a new task."""
        pass
    
    @abstractmethod
    def update_task(self, task_id: str, title: Optional[str] = None, 
                   description: Optional[str] = None, status: Optional[str] = None) -> Optional[Task]:
        """Updates an existing task."""
        pass
    
    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
        """Deletes a task by its ID."""
        pass

class AuthService(ABC):
    """Interface for the authentication service."""
    
    @abstractmethod
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticates a user and returns a JWT token."""
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> Optional[dict]:
        """Verifies a JWT token and returns the user information."""
        pass 