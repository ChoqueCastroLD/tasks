"""
MongoDB implementation of the task repository.

This module provides the MongoTaskRepository class which implements the TaskRepository
interface using MongoDB as the storage backend.
"""

from typing import List, Optional
from pymongo import MongoClient
from src.domain.interfaces import TaskRepository
from src.domain.models import Task
from src.config import MONGO_URI, DB_NAME

class MongoTaskRepository(TaskRepository):
    """
    MongoDB implementation of the task repository.
    
    This class implements the TaskRepository interface using MongoDB as the storage backend.
    It provides methods for CRUD operations on tasks.
    """
    
    def __init__(self):
        """Initialize the MongoDB task repository."""
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db.tasks
    
    def get_all(self) -> List[Task]:
        """
        Get all tasks from the database.
        
        Returns:
            List of Task objects
        """
        tasks = []
        for doc in self.collection.find():
            tasks.append(Task.from_dict(doc))
        return tasks
    
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            Task object if found, None otherwise
        """
        doc = self.collection.find_one({"task_id": task_id})
        return Task.from_dict(doc) if doc else None
    
    def save(self, task: Task) -> Task:
        """
        Save a new task to the database.
        
        Args:
            task: The Task object to save
            
        Returns:
            The saved Task object
        """
        self.collection.insert_one(task.to_dict())
        return task
    
    def update(self, task: Task) -> Task:
        """
        Update an existing task in the database.
        
        Args:
            task: The Task object with updated fields
            
        Returns:
            The updated Task object
        """
        self.collection.update_one(
            {"task_id": task.task_id},
            {"$set": task.to_dict()}
        )
        return task
    
    def delete(self, task_id: str) -> bool:
        """
        Delete a task from the database.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was deleted, False otherwise
        """
        result = self.collection.delete_one({"task_id": task_id})
        return result.deleted_count > 0 