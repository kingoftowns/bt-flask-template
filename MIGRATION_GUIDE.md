# Migration Guide for Developers

This guide explains how to modify the database schema and work with migrations when using this template.

## Understanding the Current Schema

The template includes a `User` model with:
- `id` (primary key)
- `first_name` (required)
- `last_name` (required)
- `email` (unique, required)
- `phone_number` (optional)
- `created_at` (timestamp)
- `updated_at` (timestamp)

## Step-by-Step: Modifying the Data Model

### 1. Simple Field Addition

To add a new field to the User model:

```python
# In app/models.py, add to the User class:
date_of_birth: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
```

Then create and apply migration:
```bash
flask db migrate -m "Add date_of_birth to users"
flask db upgrade
```

### 2. Creating a New Model

Example: Adding a `Post` model related to users:

```python
# In app/models.py
class Post(db.Model):
    __tablename__ = 'posts'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user: Mapped['User'] = relationship('User', back_populates='posts')

# Add to User model:
posts: Mapped[List['Post']] = relationship('Post', back_populates='user', cascade='all, delete-orphan')
```

### 3. Changing Field Types

To change a field type (e.g., String length):

```python
# Change from:
email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
# To:
email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
```

Note: Some changes may require manual migration editing.

## Common Migration Scenarios

### Adding a Required Field to Existing Table

1. First, add field as nullable:
```python
new_field: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
```

2. Migrate and set default values:
```bash
flask db migrate -m "Add new_field as nullable"
flask db upgrade
flask shell
>>> from app import db
>>> from app.models import User
>>> User.query.update({User.new_field: 'default_value'})
>>> db.session.commit()
```

3. Make field required:
```python
new_field: Mapped[str] = mapped_column(String(100), nullable=False)
```

4. Final migration:
```bash
flask db migrate -m "Make new_field required"
flask db upgrade
```

### Adding Indexes

```python
# Add index=True to improve query performance
email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

# Or composite index
__table_args__ = (
    db.Index('idx_first_last_name', 'first_name', 'last_name'),
)
```

### Adding Constraints

```python
from sqlalchemy import CheckConstraint

class Product(db.Model):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    
    __table_args__ = (
        CheckConstraint('price > 0', name='positive_price'),
    )
```

## Migration Commands Reference

```bash
# Initialize migrations (only once)
flask db init

# Create new migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback one migration
flask db downgrade

# View migration history
flask db history

# Show current migration
flask db current

# Upgrade to specific revision
flask db upgrade <revision>

# Generate SQL without applying
flask db upgrade --sql
```

## Troubleshooting Migrations

### Migration Detected No Changes

If model changes aren't detected:
1. Check imports in migration env.py
2. Manually edit migration file
3. Or delete and recreate:
```bash
flask db downgrade
# Delete the migration file
flask db migrate -m "Description"
flask db upgrade
```

### Migration Fails to Apply

Common causes:
- Data conflicts (e.g., unique constraint violations)
- Incompatible type changes
- Foreign key constraints

Solutions:
1. Create data migration first
2. Apply in steps (nullable → populate → required)
3. Manual migration editing

### Reset Database (Development Only)

```bash
# Complete reset
rm -rf migrations/
dropdb flask_app
createdb flask_app
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Best Practices

1. **Always backup before migrations in production**
2. **Test migrations on a copy of production data**
3. **Keep migrations small and focused**
4. **Write descriptive migration messages**
5. **Review auto-generated migrations before applying**
6. **Don't edit migrations after they've been applied**
7. **Use migration branches for feature development**

## Example: Complete Feature Addition

Adding a "Categories" feature to the template:

1. Create model:
```python
class Category(db.Model):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
```

2. Create API endpoints:
```python
# In app/api/categories.py
@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return {'categories': [c.to_dict() for c in categories]}, 200

@api_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    category = Category(
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(category)
    db.session.commit()
    return category.to_dict(), 201
```

3. Run migrations:
```bash
flask db migrate -m "Add categories table"
flask db upgrade
```

4. Test:
```bash
curl -X POST http://localhost:8080/api/v1/categories \
  -H "Content-Type: application/json" \
  -d '{"name": "Electronics", "description": "Electronic items"}'
```

## Need Help?

- Check Flask-Migrate documentation: https://flask-migrate.readthedocs.io/
- SQLAlchemy documentation: https://docs.sqlalchemy.org/
- Review existing migrations in `migrations/versions/` for examples