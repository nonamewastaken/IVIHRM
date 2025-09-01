from flask import Flask
import os
import logging

app = Flask(__name__)

# Set up logging with more details
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(BASE_DIR, 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Import and initialize models
from models import db
db.init_app(app)

# Create database tables
def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

# Import and register blueprints
from routes.main import main_bp
from routes.auth import auth_bp
from routes.password_reset import password_reset_bp
from routes.onboarding import onboarding_bp

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(password_reset_bp)
app.register_blueprint(onboarding_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
