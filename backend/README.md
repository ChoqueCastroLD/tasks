# Task Manager API

## Project Overview
The Task Manager API is a backend service designed to manage tasks for users. It provides endpoints for user authentication, task creation, retrieval, updating, and deletion. The API is built using Flask and MongoDB, with JWT for authentication.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following variables:
   ```
   MONGO_URI=<your-mongo-uri>
   DB_NAME=<your-database-name>
   JWT_SECRET=<your-jwt-secret>
   JWT_ALGORITHM=HS256
   JWT_EXPIRE_MINUTES=30
   CORS_ORIGINS=http://localhost:3000
   ```

## Usage

1. **Run the application**:
   ```bash
   flask run
   ```

2. **Access the API**:
   The API will be available at `http://localhost:8000`.

## API Endpoints

- **POST /auth/register**: Register a new user.
- **POST /auth/login**: Authenticate a user and receive a JWT token.
- **GET /tasks**: Retrieve all tasks.
- **GET /tasks/<task_id>**: Retrieve a specific task by ID.
- **POST /tasks**: Create a new task.
- **PUT /tasks/<task_id>**: Update an existing task.
- **DELETE /tasks/<task_id>**: Delete a task by ID.

## Configuration

- **Environment Variables**: Ensure all required environment variables are set in the `.env` file.
- **Database**: The application uses MongoDB for data storage.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push to your branch.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details. 