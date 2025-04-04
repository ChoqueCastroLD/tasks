"""
Flask application for the Task Manager API.

This module sets up the Flask application with routes for authentication and task management.
It handles request/response conversion between Flask and the internal API handlers.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from src.api.handlers import login, register, get_tasks, get_task, create_task, update_task, delete_task

load_dotenv()

app = Flask(__name__)
CORS(app)

def convert_request_to_event(flask_request, path_params=None):
    """
    Convert Flask request to the format expected by the handlers.
    
    Args:
        flask_request: The Flask request object
        path_params: Optional dictionary of path parameters
        
    Returns:
        Dict containing the converted request data
    """
    try:
        body = flask_request.get_json()
    except:
        body = {}
    
    return {
        "body": json.dumps(body or {}),
        "pathParameters": path_params or {},
        "headers": dict(flask_request.headers)
    }

def handle_handler_response(handler_response):
    """
    Convert handler response to Flask response.
    
    Args:
        handler_response: The response from the API handler
        
    Returns:
        Tuple containing the Flask response, status code, and headers
    """
    try:
        response_body = json.loads(handler_response["body"])
        headers = handler_response.get("headers", {})
        status_code = handler_response.get("statusCode", 200)
        return jsonify(response_body), status_code, headers
    except Exception as e:
        app.logger.error(f"Error handling response: {str(e)}")
        return jsonify({"error": {"message": str(e), "type": "ResponseError"}}), 500

@app.route('/auth/register', methods=['POST'])
def register_route():
    """Handle user registration."""
    event = convert_request_to_event(request)
    return handle_handler_response(register(event))

@app.route('/auth/login', methods=['POST'])
def login_route():
    """Handle user login."""
    event = convert_request_to_event(request)
    return handle_handler_response(login(event))

@app.route('/tasks', methods=['GET'])
def get_tasks_route():
    """Get all tasks."""
    event = convert_request_to_event(request)
    return handle_handler_response(get_tasks(event))

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task_route(task_id):
    """Get a specific task by ID."""
    event = convert_request_to_event(request, {"taskId": task_id})
    return handle_handler_response(get_task(event))

@app.route('/tasks', methods=['POST'])
def create_task_route():
    """Create a new task."""
    event = convert_request_to_event(request)
    return handle_handler_response(create_task(event))

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task_route(task_id):
    """Update an existing task."""
    event = convert_request_to_event(request, {"taskId": task_id})
    return handle_handler_response(update_task(event))

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    """Delete a task."""
    event = convert_request_to_event(request, {"taskId": task_id})
    return handle_handler_response(delete_task(event))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=os.getenv('DEBUG', 'False').lower() == 'true') 