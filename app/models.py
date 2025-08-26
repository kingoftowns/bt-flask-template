"""Database models for the application.

To modify or add new models:
1. Create a new class inheriting from db.Model
2. Define your columns using db.Column()
3. Add any relationships or constraints
4. Run migrations: flask db migrate -m "Description"
5. Apply migrations: flask db upgrade
"""

from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app import db


class User(db.Model):
    """User model representing application users.
    
    To modify this model:
    1. Add/remove/modify columns as needed
    2. Update the to_dict() method to include new fields
    3. Update from_dict() method for new required fields
    4. Generate and run migrations
    """
    __tablename__ = 'users'
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Required fields
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    
    # Optional fields
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self) -> str:
        """String representation of User."""
        return f'<User {self.email}>'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the user
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'User':
        """Create User instance from dictionary.
        
        Args:
            data: Dictionary containing user data
            
        Returns:
            New User instance
        """
        user = User()
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        user.email = data.get('email', '')
        user.phone_number = data.get('phone_number')
        return user
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update user fields from dictionary.
        
        Args:
            data: Dictionary containing fields to update
        """
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'email' in data:
            self.email = data['email']
        if 'phone_number' in data:
            self.phone_number = data['phone_number']