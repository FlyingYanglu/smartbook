from flask import Flask
from app.celery_app import create_celery
from smartbook.data import Data
from smartbook.llms.poe import Poe
from smartbook.booking import Booker
import os


# Initialize components globally
data_fetcher = Data()
model = Poe(headless=True)
booker = Booker(model)

def create_app():
    """Flask application factory."""
    app = Flask(__name__)

    # Celery configuration

    app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    
    # Initialize Celery
    celery = create_celery(app)

    # Import and register routes
    from app.routes import register_routes
    register_routes(app, celery)

    return app
