"""Main application entry point."""

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Run the development server
    app.run(
        host=app.config['APP_HOST'],
        port=app.config['APP_PORT'],
        debug=app.config['DEBUG']
    )