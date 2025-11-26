"""
Security utilities for encryption and hashing
"""
import hashlib
import secrets
from cryptography.fernet import Fernet
import base64


class SecurityManager:
    """Manages encryption and password hashing"""

    def __init__(self):
        # For demo: use fixed key (in production: store securely)
        # Generate with: Fernet.generate_key()
        self.key = b'zO8vH3KqW9xLm2nR5tYu7pAs1dFg4hJk6lZx8cVb0nM='
        self.cipher = Fernet(self.key)

    def hash_password(self, password: str) -> str:
        """
        Hash password using SHA-256
        In production: use bcrypt or argon2
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed

    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return data

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return encrypted_data

    def generate_token(self, length: int = 32) -> str:
        """Generate random token"""
        return secrets.token_urlsafe(length)


# Global instance
security = SecurityManager()
