import json
import os
import pytest
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from lambda_function import lambda_handler, create_task, get_tasks, update_task, delete_task, login

# Mock MongoDB connection
class MockMongoClient:
    def __init__(self):
        self.db = MockDatabase()
    
    def __getitem__(self, key):
        return self.db

class MockDatabase:
    def __init__(self):
        self.collection = MockCollection()
    
    def __getitem__(self, key):
        return self.collection

class MockCollection:
    def __init__(self):
        self.items = []
        self.next_id = 1
    
    def find(self):
        return self.items
    
    def find_one(self, query):
        for item in self.items:
            if all(item.get(k) == v for k, v in query.items()):
                return item
        return None
    
    def insert_one(self, document):
        document['_id'] = str(self.next_id)
        self.next_id += 1
        self.items.append(document)
        return type('obj', (object,), {'inserted_id': document['_id']})
    
    def update_one(self, query, update):
        for i, item in enumerate(self.items):
            if all(item.get(k) == v for k, v in query.items()):
                for key, value in update['$set'].items():
                    self.items[i][key] = value
                return type('obj', (object,), {'modified_count': 1})
        return type('obj', (object,), {'modified_count': 0})
    
    def delete_one(self, query):
        for i, item in enumerate(self.items):
            if all(item.get(k) == v for k, v in query.items()):
                del self.items[i]
                return type('obj', (object,), {'deleted_count': 1})
        return type('obj', (object,), {'deleted_count': 0})

# Mock the MongoDB client
@pytest.fixture
def mock_mongo(monkeypatch):
    mock_client = MockMongoClient()
    monkeypatch.setattr('lambda_function.MongoClient', lambda *args, **kwargs: mock_client)
    monkeypatch.setattr('lambda_function.client', mock_client)
    monkeypatch.setattr('lambda_function.db', mock_client.db)
    monkeypatch.setattr('lambda_function.collection', mock_client.db.collection)
    return mock_client

def test_login():
    # Test successful login
    event = {
        'httpMethod': 'POST',
        'path': '/login',
        'body': json.dumps({
            'username': 'admin',
            'password': 'password'
        })
    }
    context = {}
    
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    
    body = json.loads(response['body'])
    assert 'access_token' in body
    assert body['token_type'] == 'bearer'
    
    # Test failed login
    event = {
        'httpMethod': 'POST',
        'path': '/login',
        'body': json.dumps({
            'username': 'admin',
            'password': 'wrong_password'
        })
    }
    
    response = lambda_handler(event, context)
    assert response['statusCode'] == 401
    
    body = json.loads(response['body'])
    assert 'error' in body
    assert body['error'] == 'Invalid credentials'

def test_create_task(mock_mongo):
    # Test unauthorized access
    event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'TODO'
        })
    }
    context = {}
    
    response = lambda_handler(event, context)
    assert response['statusCode'] == 401
    
    # Test authorized access
    event = {
        'httpMethod': 'POST',
        'headers': {
            'Authorization': 'Bearer valid_token'
        },
        'body': json.dumps({
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'TODO'
        })
    }
    
    # Mock token verification
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('lambda_function.verify_token', lambda token: {'sub': 'admin'})
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 201
    
    body = json.loads(response['body'])
    assert 'task' in body
    assert body['task']['title'] == 'Test Task'
    assert body['task']['status'] == 'TODO'
    
    # Test missing title
    event = {
        'httpMethod': 'POST',
        'headers': {
            'Authorization': 'Bearer valid_token'
        },
        'body': json.dumps({
            'description': 'Test Description',
            'status': 'TODO'
        })
    }
    
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('lambda_function.verify_token', lambda token: {'sub': 'admin'})
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 422
    
    body = json.loads(response['body'])
    assert 'error' in body
    assert body['error'] == 'Title is required'

def test_get_tasks(mock_mongo):
    # Test unauthorized access
    event = {
        'httpMethod': 'GET'
    }
    context = {}
    
    response = lambda_handler(event, context)
    assert response['statusCode'] == 401
    
    # Test authorized access with no tasks
    event = {
        'httpMethod': 'GET',
        'headers': {
            'Authorization': 'Bearer valid_token'
        }
    }
    
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('lambda_function.verify_token', lambda token: {'sub': 'admin'})
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 200
    
    body = json.loads(response['body'])
    assert 'tasks' in body
    assert len(body['tasks']) == 0
    
    # Add a task and test getting tasks
    mock_mongo.db.collection.items.append({
        '_id': '1',
        'id': 'task1',
        'title': 'Test Task',
        'description': 'Test Description',
        'status': 'TODO',
        'created_at': '2023-01-01T00:00:00',
        'updated_at': '2023-01-01T00:00:00',
        'created_by': 'admin'
    })
    
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('lambda_function.verify_token', lambda token: {'sub': 'admin'})
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 200
    
    body = json.loads(response['body'])
    assert 'tasks' in body
    assert len(body['tasks']) == 1
    assert body['tasks'][0]['title'] == 'Test Task'

def test_update_task(mock_mongo):
    # Add a task
    mock_mongo.db.collection.items.append({
        '_id': '1',
        'id': 'task1',
        'title': 'Test Task',
        'description': 'Test Description',
        'status': 'TODO',
        'created_at': '2023-01-01T00:00:00',
        'updated_at': '2023-01-01T00:00:00',
        'created_by': 'admin'
    })
    
    # Test unauthorized access
    event = {
        'httpMethod': 'PUT',
        'pathParameters': {'id': 'task1'},
        'body': json.dumps({
            'status': 'IN_PROGRESS'
        })
    }
    context = {}
    
    response = lambda_handler(event, context)
    assert response['statusCode'] == 401
    
    # Test authorized access
    event = {
        'httpMethod': 'PUT',
        'headers': {
            'Authorization': 'Bearer valid_token'
        },
        'pathParameters': {'id': 'task1'},
        'body': json.dumps({
            'status': 'IN_PROGRESS'
        })
    }
    
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('lambda_function.verify_token', lambda token: {'sub': 'admin'})
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 200
    
    body = json.loads(response['body'])
    assert 'task' in body
    assert body['task']['status'] == 'IN_PROGRESS'
    
    # Test invalid status
    event = {
        'httpMethod': 'PUT',
        'headers': {
            'Authorization': 'Bearer valid_token'
        },
        'pathParameters': {'id': 'task1'},
        'body': json.dumps({
            'status': 'INVALID_STATUS'
        })
    }
    
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('lambda_function.verify_token', lambda token: {'sub': 'admin'})
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 422
    
    body = json.loads(response['body'])
    assert 'error' in body
    assert body['error'] == 'Invalid status'
    
    # Test non-existent task
    event = {
        'httpMethod': 'PUT',
        'headers': {
            'Authorization': 'Bearer valid_token'
        },
        'pathParameters': {'id': 'non_existent_task'},
        'body': json.dumps({
            'status': 'IN_PROGRESS'
        })
    }
    
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('lambda_function.verify_token', lambda token: {'sub': 'admin'})
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 404
    
    body = json.loads(response['body'])
    assert 'error' in body
    assert body['error'] == 'Task not found'

def test_delete_task(mock_mongo):
    # Add a task
    mock_mongo.db.collection.items.append({
        '_id': '1',
        'id': 'task1',
        'title': 'Test Task',
        'description': 'Test Description',
        'status': 'TODO',
        'created_at': '2023-01-01T00:00:00',
        'updated_at': '2023-01-01T00:00:00',
        'created_by': 'admin'
    })
    
    # Test unauthorized access
    event = {
        'httpMethod': 'DELETE',
        'pathParameters': {'id': 'task1'}
    }
    context = {}
    
    response = lambda_handler(event, context)
    assert response['statusCode'] == 401
    
    # Test authorized access
    event = {
        'httpMethod': 'DELETE',
        'headers': {
            'Authorization': 'Bearer valid_token'
        },
        'pathParameters': {'id': 'task1'}
    }
    
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('lambda_function.verify_token', lambda token: {'sub': 'admin'})
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 204
    
    # Verify task is deleted
    assert len(mock_mongo.db.collection.items) == 0
    
    # Test non-existent task
    event = {
        'httpMethod': 'DELETE',
        'headers': {
            'Authorization': 'Bearer valid_token'
        },
        'pathParameters': {'id': 'non_existent_task'}
    }
    
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('lambda_function.verify_token', lambda token: {'sub': 'admin'})
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 404
    
    body = json.loads(response['body'])
    assert 'error' in body
    assert body['error'] == 'Task not found' 