from flask import Flask
from flask_cors import CORS
import os
import logging
from config.settings import config
from core.database import db, init_database
# Import models to register them with SQLAlchemy
import models

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__, 
                static_folder='shared/static',
                template_folder='shared/templates')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Set up logging with more details
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    # Initialize database
    init_database(app)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Import and register blueprints
    from features.auth import auth_bp
    from features.dashboard import dashboard_bp
    from features.onboarding import onboarding_bp
    from features.password_reset import password_reset_bp
    from features.attendance import attendance_bp
    from features.administrative_personnel import administrative_personnel_bp
    from features.salary import salary_bp
    from features.decision import decision_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(onboarding_bp)
    app.register_blueprint(password_reset_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(administrative_personnel_bp)
    app.register_blueprint(salary_bp)
    app.register_blueprint(decision_bp)
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001,host='0.0.0.0')
