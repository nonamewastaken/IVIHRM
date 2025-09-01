from flask_sqlalchemy import SQLAlchemy
from config.settings import config

db = SQLAlchemy()

def init_database(app):
    """Initialize database with the Flask app"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")
