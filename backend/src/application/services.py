from typing import List, Optional
from datetime import datetime

from ..domain.interfaces import TaskService
from ..domain.models import Task

class TaskServiceImpl(TaskService):
    """Implementación del servicio de tareas."""
    
    def __init__(self, task_repository):
        """Inicializa el servicio de tareas con un repositorio."""
        self.task_repository = task_repository
    
    def get_all_tasks(self) -> List[Task]:
        """Obtiene todas las tareas."""
        return self.task_repository.get_all()
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Obtiene una tarea por su ID."""
        return self.task_repository.get_by_id(task_id)
    
    def create_task(self, title: str, description: str, status: str, user_id: str) -> Task:
        """Crea una nueva tarea."""
        task = Task(
            title=title,
            description=description,
            status=status,
            created_by=user_id
        )
        return self.task_repository.save(task)
    
    def update_task(self, task_id: str, title: Optional[str] = None,
                   description: Optional[str] = None, status: Optional[str] = None) -> Optional[Task]:
        """Actualiza una tarea existente."""
        task = self.task_repository.get_by_id(task_id)
        if not task:
            return None
            
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if status is not None:
            update_data['status'] = status
            
        task.update(**update_data)
        return self.task_repository.update(task)
    
    def delete_task(self, task_id: str) -> bool:
        """Elimina una tarea por su ID."""
        return self.task_repository.delete(task_id) 