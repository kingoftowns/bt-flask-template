# Flask PostgreSQL Template

Production-ready Flask template with PostgreSQL, SQLAlchemy, and DevContainer support.

## Quick Start

### Using DevContainers (Recommended)
1. Open in VS Code with DevContainers extension
2. Click "Reopen in Container" when prompted
3. Press F5 to start debugging
4. Visit http://localhost:8080/docs for API documentation

### Local Development
```bash
# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run application
flask run
```

## Project Structure

```
flask-template/
├── app/
│   ├── __init__.py        # App factory
│   ├── models.py          # Database models
│   └── api/               # API endpoints
│       └── users.py       # User CRUD endpoints
├── config.py              # Configuration
├── app.py                 # Entry point
└── requirements.txt       # Dependencies
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users` | List all users |
| GET | `/api/v1/users/{id}` | Get specific user |
| POST | `/api/v1/users` | Create new user |
| PUT | `/api/v1/users/{id}` | Update user |
| DELETE | `/api/v1/users/{id}` | Delete user |
| GET | `/docs` | Interactive API documentation |

See `tests.http` file for example requests that you can run directly in VS Code.

## Customization

### Changing Database Schema
1. Edit `app/models.py`:
```python
class YourModel(db.Model):
    __tablename__ = 'your_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
```

2. Generate and apply migration:
```bash
flask db migrate -m "Add your model"
flask db upgrade
```

### Adding New Endpoints
Create a new file in `app/api/` or add to existing:
```python
from app.api import api_bp

@api_bp.route('/your-endpoint', methods=['GET'])
def your_function():
    return {'data': 'value'}, 200
```

## Environment Variables

Key variables in `.env`:
- `DATABASE_URL` or individual DB settings (`DB_HOST`, `DB_NAME`, etc.)
- `SECRET_KEY` for session security
- `FLASK_ENV` (development/production)
- `DEBUG` for debug mode

## Common Commands

```bash
# Database migrations
flask db migrate -m "Description"  # Create migration
flask db upgrade                    # Apply migration
flask db downgrade                  # Rollback

# Testing
pytest                              # Run tests
pytest --cov=app                    # With coverage

# Production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## License

MIT - Use this template for your projects!