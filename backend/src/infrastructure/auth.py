"""
Authentication service implementation using JWT tokens.

This module provides the JwtAuthService class which handles user authentication,
token generation, and token verification using JSON Web Tokens (JWT).
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import jwt, JWTError

from ..domain.interfaces import AuthService
from src.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

class JwtAuthService(AuthService):
    """
    JWT-based authentication service.
    
    This class implements the AuthService interface using JWT tokens for authentication.
    It provides methods for user registration, authentication, and token verification.
    """
    
    def __init__(self):
        """Initialize the JWT authentication service."""
        self.users = {}
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """
        Authenticate a user and return a JWT token.
        
        Args:
            username: The username to authenticate
            password: The password to verify
            
        Returns:
            JWT token if authentication is successful, None otherwise
        """
        if username in self.users and self.users[username] == password:
            return self._create_token(username)
        return None
    
    def register(self, username: str, password: str) -> str:
        """
        Register a new user and return a JWT token.
        
        Args:
            username: The username to register
            password: The password to store
            
        Returns:
            JWT token for the newly registered user
        """
        self.users[username] = password
        return self._create_token(username)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a JWT token and return the user information.
        
        Args:
            token: The JWT token to verify
            
        Returns:
            Dictionary containing user information if token is valid, None otherwise
        """
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.InvalidTokenError:
            return None
    
    def _create_token(self, username: str) -> str:
        """
        Create a new JWT token for a user.
        
        Args:
            username: The username to create a token for
            
        Returns:
            JWT token string
        """
        payload = {
            "user_id": username,
            "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM) 