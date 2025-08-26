#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
    sleep 1
done

echo "PostgreSQL is ready!"

# Check if migrations folder exists
if [ ! -d "migrations" ]; then
    echo "Initializing database migrations..."
    flask db init
fi

# Always try to create and apply migrations
echo "Creating migration if model changes exist..."
flask db migrate -m "Auto migration" || true

echo "Applying database migrations..."
flask db upgrade

echo "Database is ready!"

# Execute the command passed to docker run
exec "$@"