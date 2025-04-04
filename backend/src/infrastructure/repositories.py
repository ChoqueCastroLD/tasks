from typing import List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from ..domain.interfaces import TaskRepository
from ..domain.models import Task

class MongoTaskRepository(TaskRepository):
    """Implementación del repositorio de tareas usando MongoDB."""
    
    def __init__(self, mongo_uri: str, db_name: str, collection_name: str):
        """Inicializa el repositorio con la conexión a MongoDB."""
        self.client = MongoClient(mongo_uri)
        self.db: Database = self.client[db_name]
        self.collection: Collection = self.db[collection_name]
    
    def get_all(self) -> List[Task]:
        """Obtiene todas las tareas."""
        tasks_data = list(self.collection.find())
        return [Task.from_dict(task_data) for task_data in tasks_data]
    
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Obtiene una tarea por su ID."""
        task_data = self.collection.find_one({"id": task_id})
        if task_data:
            return Task.from_dict(task_data)
        return None
    
    def save(self, task: Task) -> Task:
        """Guarda una tarea."""
        task_dict = task.to_dict()
        result = self.collection.insert_one(task_dict)
        task_dict["_id"] = str(result.inserted_id)
        return Task.from_dict(task_dict)
    
    def update(self, task: Task) -> Task:
        """Actualiza una tarea."""
        task_dict = task.to_dict()
        self.collection.update_one(
            {"id": task.id},
            {"$set": task_dict}
        )
        return task
    
    def delete(self, task_id: str) -> bool:
        """Elimina una tarea por su ID."""
        result = self.collection.delete_one({"id": task_id})
        return result.deleted_count > 0 