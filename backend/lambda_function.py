import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from jose import jwt, JWTError
from pymongo import MongoClient
from bson import ObjectId

# MongoDB configuration
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'task_management')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'tasks')

# JWT configuration
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-for-development')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def create_response(status_code: int, body: Dict, headers: Dict = None) -> Dict:
    response_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': True,
    }
    if headers:
        response_headers.update(headers)
    
    return {
        'statusCode': status_code,
        'headers': response_headers,
        'body': json.dumps(body)
    }

def verify_token(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def authenticate_request(event: Dict) -> Optional[Dict]:
    auth_header = event.get('headers', {}).get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    return verify_token(token)

def login(event, context):
    try:
        credentials = json.loads(event['body'])
        username = credentials.get('username')
        password = credentials.get('password')
        
        # hardcoded credentials
        if username == 'admin' and password == 'password':
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": username}, expires_delta=access_token_expires
            )
            return create_response(200, {"access_token": access_token, "token_type": "bearer"})
        else:
            return create_response(401, {"error": "Invalid credentials"})
    except Exception as e:
        return create_response(500, {"error": str(e)})

def create_access_token(data: Dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_tasks(event, context):
    try:
        # Authentication check
        user = authenticate_request(event)
        if not user:
            return create_response(401, {"error": "Unauthorized"})
            
        tasks = list(collection.find())
        # Convert ObjectId to string for JSON serialization
        for task in tasks:
            task['_id'] = str(task['_id'])
            
        return create_response(200, {'tasks': tasks})
    except Exception as e:
        return create_response(500, {'error': str(e)})

def create_task(event, context):
    try:
        # Authentication check
        user = authenticate_request(event)
        if not user:
            return create_response(401, {"error": "Unauthorized"})
            
        task_data = json.loads(event['body'])
        
        # Validate required fields
        if not task_data.get('title'):
            return create_response(422, {'error': 'Title is required'})
            
        task = {
            'id': str(uuid.uuid4()),
            'title': task_data['title'],
            'description': task_data.get('description', ''),
            'status': task_data.get('status', 'TODO'),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'created_by': user.get('sub', 'unknown')
        }
        
        result = collection.insert_one(task)
        task['_id'] = str(result.inserted_id)
        
        return create_response(201, {'task': task})
    except Exception as e:
        return create_response(500, {'error': str(e)})

def update_task(event, context):
    try:
        # Authentication check
        user = authenticate_request(event)
        if not user:
            return create_response(401, {"error": "Unauthorized"})
            
        task_id = event['pathParameters']['id']
        updates = json.loads(event['body'])
        
        # Validate status if provided
        if 'status' in updates and updates['status'] not in ['TODO', 'IN_PROGRESS', 'COMPLETED']:
            return create_response(422, {'error': 'Invalid status'})
        
        # Prepare update document
        update_doc = {}
        for key, value in updates.items():
            if key in ['title', 'description', 'status']:
                update_doc[key] = value
        
        update_doc['updated_at'] = datetime.utcnow().isoformat()
        
        # Find task by ID
        task = collection.find_one({'id': task_id})
        if not task:
            return create_response(404, {'error': 'Task not found'})
        
        # Update task
        result = collection.update_one(
            {'id': task_id},
            {'$set': update_doc}
        )
        
        if result.modified_count == 0:
            return create_response(404, {'error': 'Task not found'})
        
        # Get updated task
        updated_task = collection.find_one({'id': task_id})
        updated_task['_id'] = str(updated_task['_id'])
        
        return create_response(200, {'task': updated_task})
    except Exception as e:
        return create_response(500, {'error': str(e)})

def delete_task(event, context):
    try:
        # Authentication check
        user = authenticate_request(event)
        if not user:
            return create_response(401, {"error": "Unauthorized"})
            
        task_id = event['pathParameters']['id']
        
        # Find task by ID
        task = collection.find_one({'id': task_id})
        if not task:
            return create_response(404, {'error': 'Task not found'})
        
        # Delete task
        result = collection.delete_one({'id': task_id})
        
        if result.deleted_count == 0:
            return create_response(404, {'error': 'Task not found'})
        
        return create_response(204, {})
    except Exception as e:
        return create_response(500, {'error': str(e)})

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == 'POST' and event.get('path', '') == '/login':
        return login(event, context)
    elif http_method == 'GET':
        return get_tasks(event, context)
    elif http_method == 'POST':
        return create_task(event, context)
    elif http_method == 'PUT':
        return update_task(event, context)
    elif http_method == 'DELETE':
        return delete_task(event, context)
    else:
        return create_response(405, {'error': 'Method not allowed'}) 