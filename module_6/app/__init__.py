"""app/__init__.py: application factory and blueprint registration."""
from flask import Flask
from .main.routes import main as main_blueprint

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.register_blueprint(main_blueprint)

    return app
