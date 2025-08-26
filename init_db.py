#!/usr/bin/env python
"""Initialize database with migrations.

Run this script to set up the database with migrations.
This is useful for debugging or when you need to manually initialize the database.
"""

import os
import sys
import time
from subprocess import run, CalledProcessError

def wait_for_db():
    """Wait for database to be ready."""
    print("Waiting for PostgreSQL to be ready...")
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        result = run(
            ["pg_isready", "-h", os.getenv("DB_HOST", "localhost"), 
             "-p", os.getenv("DB_PORT", "5432"), 
             "-U", os.getenv("DB_USER", "postgres")],
            capture_output=True
        )
        
        if result.returncode == 0:
            print("PostgreSQL is ready!")
            return True
        
        attempt += 1
        time.sleep(1)
    
    print("Failed to connect to PostgreSQL after 30 seconds")
    return False

def init_migrations():
    """Initialize and run migrations."""
    try:
        # Check if migrations folder exists
        if not os.path.exists("migrations"):
            print("Initializing database migrations...")
            run(["flask", "db", "init"], check=True)
        
        # Create migration
        print("Creating migration if model changes exist...")
        run(["flask", "db", "migrate", "-m", "Auto migration"])
        
        # Apply migrations
        print("Applying database migrations...")
        run(["flask", "db", "upgrade"], check=True)
        
        print("Database is ready!")
        return True
        
    except CalledProcessError as e:
        print(f"Error during migration: {e}")
        return False

if __name__ == "__main__":
    if wait_for_db():
        if init_migrations():
            print("Database initialization complete!")
            sys.exit(0)
        else:
            print("Failed to initialize database")
            sys.exit(1)
    else:
        print("Database connection failed")
        sys.exit(1)