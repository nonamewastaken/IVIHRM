import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DB_FILE = os.path.join(BASE_DIR, 'users.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE}'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Add production database URI here
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
