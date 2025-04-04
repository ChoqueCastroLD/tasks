# Task Manager Project

## Project Overview
The Task Manager Project is a full-stack application that allows users to manage tasks. It consists of a backend API built with Flask and a frontend application built with React. The project uses MongoDB for data storage and JWT for authentication.

## Prerequisites

- **Docker**: Ensure Docker is installed on your system. You can download it from [Docker's official website](https://www.docker.com/get-started).
- **Docker Compose**: Docker Compose should be installed along with Docker.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root directory and add the necessary environment variables for both the backend and frontend.

## Usage

1. **Run the application**:
   Use Docker Compose to build and start the application:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   - The frontend will be available at `http://localhost:3000`.
   - The backend API will be available at `http://localhost:8000`.

## Configuration

- **Environment Variables**: Ensure all required environment variables are set in the `.env` file.
- **Docker Compose**: The `docker-compose.yml` file should be configured to set up the services correctly.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push to your branch.
5. Create a pull request.
