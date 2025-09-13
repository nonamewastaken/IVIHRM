from flask_sqlalchemy import SQLAlchemy
from config.settings import config

db = SQLAlchemy()

def init_database(app):
    """Initialize database with the Flask app"""
    db.init_app(app)
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Database initialized successfully!")
            print("Tables created:", db.metadata.tables.keys())
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise e
