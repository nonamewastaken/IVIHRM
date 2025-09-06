from flask import Flask
import os
import logging
from config.settings import config
from core.database import db, init_database

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
    
    # Import and register blueprints
    from features.auth import auth_bp
    from features.dashboard import dashboard_bp
    from features.onboarding import onboarding_bp
    from features.password_reset import password_reset_bp
    from features.attendance import attendance_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(onboarding_bp)
    app.register_blueprint(password_reset_bp)
    app.register_blueprint(attendance_bp)
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)