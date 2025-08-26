"""Simple User API with automatic docs."""

from flask import request
from flask_restx import Namespace, Resource
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User

# Create namespace - this gives you automatic docs
ns = Namespace('users', description='User operations')


@ns.route('')
class UsersList(Resource):
    def get(self):
        """Get all users"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        pagination = User.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return {
            'users': [user.to_dict() for user in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }

    def post(self):
        """Create a new user"""
        data = request.json
        
        # Basic validation
        required = ['first_name', 'last_name', 'email']
        if not all(field in data for field in required):
            return {'error': 'Missing required fields'}, 400
        
        user = User.from_dict(data)
        
        try:
            db.session.add(user)
            db.session.commit()
            return user.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Email already exists'}, 409


@ns.route('/<int:user_id>')
class UserItem(Resource):
    def get(self, user_id):
        """Get user by ID"""
        user = User.query.get_or_404(user_id)
        return user.to_dict()

    def put(self, user_id):
        """Update user"""
        user = User.query.get_or_404(user_id)
        data = request.json
        
        try:
            user.update_from_dict(data)
            db.session.commit()
            return user.to_dict()
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Email already exists'}, 409

    def delete(self, user_id):
        """Delete user"""
        user = User.query.get_or_404(user_id)
        
        try:
            db.session.delete(user)
            db.session.commit()
            return {'message': f'User {user_id} deleted'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500