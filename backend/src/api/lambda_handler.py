from typing import Dict, Any
from http import HTTPStatus

from .handlers import (
    login, get_tasks, get_task,
    create_task, update_task, delete_task
)

def lambda_handler(event: Dict, context: Any) -> Dict:
    """
    Manejador principal de Lambda que enruta las solicitudes a los manejadores específicos.
    """
    http_method = event.get("httpMethod", "").upper()
    path = event.get("path", "")

    if path == "/login" and http_method == "POST":
        return login(event, context)
    
    if path == "/tasks":
        if http_method == "GET":
            return get_tasks(event, context)
        elif http_method == "POST":
            return create_task(event, context)
    
    if path.startswith("/tasks/"):
        task_id = path.split("/")[-1]
        if http_method == "GET":
            return get_task(event, context)
        elif http_method == "PUT":
            return update_task(event, context)
        elif http_method == "DELETE":
            return delete_task(event, context)

    return {
        "statusCode": HTTPStatus.NOT_FOUND,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": '{"error": "Not Found"}'
    } 