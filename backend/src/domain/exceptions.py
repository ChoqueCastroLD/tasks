class TaskManagerException(Exception):
    """Base exception for the task management system."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class AuthenticationError(TaskManagerException):
    """Authentication error."""
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, status_code=401)

class AuthorizationError(TaskManagerException):
    """Authorization error."""
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status_code=403)

class ValidationError(TaskManagerException):
    """Data validation error."""
    def __init__(self, message: str, errors: dict = None):
        self.errors = errors or {}
        super().__init__(message, status_code=422)

class ResourceNotFoundError(TaskManagerException):
    """Error when a resource is not found."""
    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message, status_code=404)

class DatabaseError(TaskManagerException):
    """Database error."""
    def __init__(self, message: str = "Database error occurred"):
        super().__init__(message, status_code=500) 