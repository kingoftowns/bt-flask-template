"""Flask application factory and initialization."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from typing import Optional

from config import get_config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
docs_api = Api(doc='/docs/', title='User API', version='1.0')


def create_app(config_name: Optional[str] = None) -> Flask:
    """Application factory pattern for Flask app creation.
    
    Args:
        config_name: Configuration environment name (development, production, testing)
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config()
    app.config.from_object(config_class)
    config_class.init_app(app)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    docs_api.init_app(app)
    
    # Register API namespace
    from app.api.users import ns as users_ns
    docs_api.add_namespace(users_ns, path='/api/v1')
    
    # Register health check endpoint
    @app.route('/health')
    def health_check():
        """Simple health check endpoint."""
        return {'status': 'healthy'}
    
    return app